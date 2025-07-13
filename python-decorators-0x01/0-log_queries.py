#!/usr/bin/env python3
import sqlite3
import functools

def log_queries(func):
    """Decorator that logs SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Assuming first argument is the SQL query string
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        if query:
            print(f"Executing SQL query: {query}")
        else:
            print("No SQL query provided.")
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
