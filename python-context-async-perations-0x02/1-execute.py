#!/usr/bin/env python3
"""
1-execute.py
Reusable query context manager for executing SQL and returning results.
"""

import sqlite3

class ExecuteQuery:
    def __init__(self, query, param):
        self.query = query
        self.param = param
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, (self.param,))
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(query, 25) as results:
        print(results)

