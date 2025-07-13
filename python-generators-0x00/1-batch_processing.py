#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from user_data table
    Yields one user at a time from each batch
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # Replace with your username if needed
            password='',       # Replace with your password if needed
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            for row in rows:
                yield {
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'age': row[3]
                }

    except Error as e:
        print(f"Database error: {e}")
        return

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches, yielding only users over age 25
    """
    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            yield user
