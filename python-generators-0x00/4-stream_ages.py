#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """
    Generator function that streams user ages one by one from the database
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield age

    except Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def compute_average_age():
    """
    Computes and prints the average age using the stream_user_ages generator
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found in database")


if __name__ == "__main__":
    compute_average_age()
