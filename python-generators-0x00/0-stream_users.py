#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that fetches rows one by one from user_data table
    Yields each row as a dictionary
    """
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # replace if needed
            password='',       # replace if needed
            database='ALX_prodev'
        )
        cursor = connection.cursor()

        # Execute select query
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # Use a single loop to fetch and yield one row at a time
        row = cursor.fetchone()
        while row:
            yield {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }
            row = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Always close resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
