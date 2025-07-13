#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    """Custom context manager that executes a given SQL query with parameters."""

    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.conn = sqlite3.connect('users.db')
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection regardless of success or error."""
        if self.conn:
            self.conn.close()

# Use the context manager to run a parameterized query
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print(results)
