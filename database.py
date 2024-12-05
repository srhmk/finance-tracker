import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yes', #Default password 
    'database': 'finance_tracker'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

#To do: Check whether it is safe to upload this file in github
