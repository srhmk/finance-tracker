import tkinter as tk
from tkinter import messagebox, Toplevel
from auth import register_user, login_user
from dashboard import open_main_window2
from PIL import Image, ImageTk

#Main Application Window
app = tk.Tk()
app.title("SHC Finance Tracker - Login and Registration")
app.geometry("500x550")
app.configure(bg='#1B2838')
app.resizable(False, False)

current_username = None
login_attempts = 3 

#For buttons and labels
i = Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\logo.png")
image=i.resize((200,200))
photologo= ImageTk.PhotoImage(image)
app.iconbitmap(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\favicon.ico")

rounded_button_image1=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\button1.png")
resized_image1 = rounded_button_image1.resize((130, 48))
photo1 = ImageTk.PhotoImage(resized_image1)

rounded_button_image2=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\button2.png")
resized_image2 = rounded_button_image2.resize((130, 48))
photo2 = ImageTk.PhotoImage(resized_image2)

#Registration Window
def open_registration():
    reg_window = Toplevel(app)
    reg_window.title("Register")
    reg_window.geometry("400x300")
    reg_window.configure(bg='#1B2838')
    reg_window.resizable(False, False)
    reg_window.iconbitmap(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\favicon.ico")
    
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()

        if len(username) < 4:
            messagebox.showerror("Error", "Username must be at least 4 characters.")
            return
        if len(password) < 8 or not any(char.isdigit() for char in password):
            messagebox.showerror("Error", "Password must be at least 8 characters and contain a number.")
            return

        success, msg = register_user(username, password)
        if success:
            messagebox.showinfo("Login to access", msg)
            reg_window.after(1500, reg_window.destroy)
        else:
            messagebox.showerror("Error", msg)

    tk.Label(reg_window,text='REGISTER:',bg='#1B2838',relief="flat", borderwidth=0,fg='white',font=('Impact',30)).pack(pady=20)

    tk.Label(reg_window, text="Username-",bg='#1B2838',relief="flat", borderwidth=0,fg='white',font=('Helvetica',10)).pack(pady=10)
    username_entry = tk.Entry(reg_window)
    username_entry.pack(pady=3)
    
    tk.Label(reg_window, text="Password-",bg='#1B2838',relief="flat", borderwidth=0,fg='white',font=('Helvetica',10)).pack(pady=10)
    password_entry = tk.Entry(reg_window, show="*")
    password_entry.pack(pady=3)

    tk.Button(reg_window, text="Submit", relief="flat", borderwidth=0, command=submit_registration).pack(pady=15)

#Login Window
def open_login():
    global login_attempts
    login_window = Toplevel(app)
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg='#1B2838')
    login_window.resizable(False, False)
    login_window.iconbitmap(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\favicon.ico")

    def submit_login():
        global current_username, login_attempts
        username = username_entry.get()
        password = password_entry.get()
        
        username, msg = login_user(username, password)
        if username:
            current_username = username
            login_window.destroy()
            app.withdraw()
            open_main_window2(username)  #Open Dashboard if login successful
        else:
            login_attempts -= 1
            if login_attempts <= 0:
                messagebox.showerror("Error", "Too many attempts, login failed.")
                login_window.destroy()
            else:
                messagebox.showerror("Error", f"{msg}. {login_attempts} attempts left.")
    
    tk.Label(login_window,text='LOGIN:',bg='#1B2838',relief="flat", borderwidth=0,fg='white',font=('Impact',30)).pack(pady=20)

    tk.Label(login_window,text="Username-",bg='#1B2838',relief="flat", borderwidth=0,fg='white',font=('Helvetica',10)).pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=3)
    
    tk.Label(login_window,text="Password-",bg='#1B2838',relief="flat", borderwidth=0,fg='white',font=('Helvetica',10)).pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=3)

    tk.Button(login_window, text="Login",relief="flat", borderwidth=0, command=submit_login).pack(pady=15)

label = tk.Label(app, image=photologo,bg='#1B2838',relief="flat", borderwidth=0)
label.place(x=150, y=45)

#Buttons for Main Window 1
tk.Button(app, text="Register", command=open_registration, image=photo1,bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=app.cget("bg"), activebackground='#1B2838').place(x=186, y=275)
tk.Button(app, text="Login", command=open_login, image=photo2,bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=app.cget("bg"), activebackground='#1B2838').place(x=186, y=350)
tk.Label(app, text="Alpha version 1.12.10",font=("Arial"),fg='grey',bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=app.cget("bg"), activebackground='#1B2838').pack(side='bottom')

app.mainloop()