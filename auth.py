# auth.py
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

# Register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return True, "Account created successfully!"
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

# Login existing user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return user['username'], "Login successful!"
    return None, "Invalid username or password"
