from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from tkinter import messagebox

#Register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute("SELECT username FROM users WHERE username=%s", (str(username),))
    details = cursor.fetchone()
    if details is None: #Checks whether username already exists
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            return True, "Account created successfully!"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    else: 
        messagebox.showerror('Error','Multiple username detected')
        cursor.close()
        conn.close()

#Login existing user
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    print(user,user['password'], password )
    cursor.close()
    conn.close()
    try:
        if user and check_password_hash(user['password'], password):
            print(user,user['password'], password )
            return user['username'], "Login successful!"
        return None, "Invalid username or password"
    except Exception as e:
        messagebox.showerror('Error', 'Unexpected Error')
        return None, e
login_user('Srihari','qwerty1234')