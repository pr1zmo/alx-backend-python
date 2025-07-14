#!/usr/bin/env python3
"""
test_client.py
Unit and integration tests for GithubOrgClient.
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([("google",), ("abc",)])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"login": org_name}
        result = GithubOrgClient(org_name).org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        url = "https://api.github.com/orgs/foo/repos"
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": url}
            self.assertEqual(
                GithubOrgClient("foo")._public_repos_url,
                url
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        repos_payload = [{"name": "r1"}, {"name": "r2"}]
        mock_get_json.return_value = repos_payload
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "ignored"
            names = GithubOrgClient("foo").public_repos()
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("ignored")
            self.assertEqual(names, ["r1", "r2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("foo")
        self.assertEqual(
            client.has_license(repo, license_key),
            expected
        )


@parameterized_class([{
    "org_payload": fixtures.org_payload,
    "repos_payload": fixtures.repos_payload,
    "expected_repos": fixtures.expected_repos,
    "apache2_repos": fixtures.apache2_repos,
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch(
            "client.requests.get",
            side_effect=[
                Mock(json=Mock(return_value=cls.org_payload)),
                Mock(json=Mock(return_value=cls.repos_payload)),
            ]
        )
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("foo")
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        client = GithubOrgClient("foo")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()

