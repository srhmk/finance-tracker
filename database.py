import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yes', #Default password 
    'database': 'finance_tracker'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        balance INT NOT NULL DEFAULT 0
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        user_id VARCHAR(50),
        date DATE,
        amount INT NOT NULL,
        category VARCHAR(30),
        description VARCHAR(30)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credits (
        user_id VARCHAR(50),
        amt INT NOT NULL,
        due_date DATE,
        status VARCHAR(20),
        no VARCHAR(30)
    )
    """)
    conn.commit()
    cursor.close()
    return conn


#To do: Check whether it is safe to upload this file in github
