#!/usr/bin/env python3
"""
0-databaseconnection.py
Class-based context manager for database connections.
"""

import sqlite3

class DatabaseConnection:
	def __init__(self, db_file='users.db'):
		self.db_file = db_file
		self.conn = None

	def __enter__(self):
		self.conn = sqlite3.connect(self.db_file)
		return self.conn

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.conn:
			self.conn.close()

if __name__ == '__main__':
	with DatabaseConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		results = cursor.fetchall()
		print(results)
