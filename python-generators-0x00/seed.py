#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    """Connect to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # replace with your MySQL password if any
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # replace if needed
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
    return None


def create_table(connection):
    """Create user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, filename):
    """Insert data from CSV file into user_data table"""
    try:
        cursor = connection.cursor()
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Check for duplicate email before inserting
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                result = cursor.fetchone()
                if not result:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()


def stream_users(connection):
    """Generator that yields one row at a time from user_data"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        cursor.close()
