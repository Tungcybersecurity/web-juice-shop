import sqlite3
import os

db_path = 'D:/CTF/Juice-shop-python/data/database.db'

def get_connection():
    try:
        with sqlite3.connect(db_path) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            return conn
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def close_connection(conn):
    if conn:
        conn.close()


