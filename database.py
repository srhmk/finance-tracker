# database.py
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yes',
    'database': 'finance_tracker'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
