from parameterized import parameterized_class
from unittest import TestCase
from client import GithubOrgClient
import requests
import fixtures

@parameterized_class([
    {"org_payload": fixtures.org_payload,
     "repos_payload": fixtures.repos_payload,
     "expected_repos": fixtures.expected_repos,
     "apache2_repos": fixtures.apache2_repos},
])
class TestIntegrationGithubOrgClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get",
                                side_effect=[
                                    Mock(json=Mock(return_value=cls.org_payload)),
                                    Mock(json=Mock(return_value=cls.repos_payload)),
                                ])
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("foo")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("foo")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)

