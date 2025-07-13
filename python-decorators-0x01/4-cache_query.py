#!/usr/bin/env python3
import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator that opens a SQLite connection, passes it to the function, and closes it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator that caches the result of a DB query based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the query string (assumes it's passed as a keyword arg 'query' or positional arg)
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        else:
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            print("Caching result for query.")
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users based on a given query string."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — will execute and cache result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call — will use cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
