#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for opening and closing a SQLite database connection."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection on exit."""
        if self.conn:
            self.conn.close()

# Use the context manager to query the users table
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
