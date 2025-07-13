#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime  # ✅ required import

def log_queries(func):
    """Decorator that logs SQL queries with a timestamp before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve the query string
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetch all users from the database based on the query"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
