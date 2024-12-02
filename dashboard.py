# dashboard.py
import tkinter as tk
from tkinter import Toplevel, StringVar, OptionMenu, messagebox
from datetime import datetime
import mysql.connector
from database import get_db_connection
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import time 
# Open Main Window 2 with enhanced functionalities
def open_main_window2(username):
    main_window2 = tk.Toplevel()
    main_window2.title("Finance Tracker - Main Dashboard")
    main_window2.geometry("800x500")
    main_window2.configure(bg='#1B2838')

    # Fetch balance from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username,balance FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    username = str(user['username'])
    balance_amount = user['balance']
    cursor.close()
    conn.close()

    # Welcome Message and Date Display
    welcome_label = tk.Label(main_window2, text=f"Welcome, {username}", font=("Copperplate Gothic Bold", 30),bg='#1B2838',fg='white')
    welcome_label.pack(pady=(10,10))

    date_label = tk.Label(main_window2, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Comic Sans MS", 15,), bg='#1B2838',fg='white')
    date_label.pack(pady=(0,5))

    # Balance Display
    balance_label = tk.Label(main_window2, text=f"Balance: {balance_amount:.2f}₹", font=("Ink Free", 25), fg="green", bg='#1B2838',)
    balance_label.pack(pady=(0,1))
    description = tk.Label(main_window2, text=f"(View balance through manage finance\nincase it doesnt refresh!!)", font=("@MS UI Gothic", 8), fg="orange", bg="#1B2838")
    description.pack()
    
    def update_balance_display():
    # Fetch the latest balance from the database
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        balance_amount = user['balance']
        cursor.close()
        conn.close()

        # Update the balance label
        balance_label.config(text=f"Balance: {balance_amount:.2f}₹")

        # Schedule the next update
        main_window2.after(3000, update_balance_display)

    # Expense History
    def view_expense_history():
        history_window = Toplevel(main_window2)
        history_window.title("Expense History")
        history_window.geometry("400x300")
        history_window.configure(bg='#1B2838')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, amount, category, description FROM transactions WHERE user_id = %s ORDER BY date DESC", (username,))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()

        scroll = tk.Scrollbar(history_window, bg='#1B2838')
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(history_window, yscrollcommand=scroll.set, bg='#1B2838', fg='red', font=('Sylfaen', 10))
        listbox.pack(fill=tk.BOTH, expand=1,side="top")

        for trans in transactions:
            listbox.insert(tk.END, f"{trans[0]} | ${trans[1]:.2f} | {trans[2]} | {trans[3]}")

        scroll.config(command=listbox.yview)

    # Credit Management
    def manage_credits():
        credit_window = Toplevel(main_window2)
        credit_window.title("Manage Credits")
        credit_window.geometry("400x300")
        credit_window.configure(bg='#1B2838')

        a=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\AddCredit.png")
        a1 = a.resize((150, 45))
        a2 = ImageTk.PhotoImage(a1)

        b=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\PendingCredits.png")
        b1 = b.resize((150, 45))
        b2 = ImageTk.PhotoImage(b1)

        c=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\CompletedCredits.png")
        c1 = c.resize((150, 45))
        c2 = ImageTk.PhotoImage(c1)

        A=tk.Button(credit_window, text="Add Credit", command=add_credit, image=a2, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
        A.image=a2
        A.place(x=135,y=50)
        B=tk.Button(credit_window, text="Pending Credits", command=view_pending_credits, image=b2, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
        B.image=b2
        B.place(x=135,y=125)
        C=tk.Button(credit_window, text="Completed Credits", command=view_completed_credits,image=c2, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
        C.image=c2
        C.place(x=135,y=200)

    def add_credit():
        add_credit_window = Toplevel(main_window2)
        add_credit_window.title("Add Credit")
        add_credit_window.geometry("300x230")
        add_credit_window.configure(bg='#1B2838')

        tk.Label(add_credit_window, text="Amount:",bg='#1B2838',fg='yellow',font=('Bahnschrift SemiBold SemiConden',15)).pack()
        amount_entry = tk.Entry(add_credit_window)
        amount_entry.pack()
        
        tk.Label(add_credit_window, text="Due Date (YYYY-MM-DD):",bg='#1B2838',fg='white',font=('Bahnschrift SemiBold SemiConden',15)).pack()
        due_date_entry = tk.Entry(add_credit_window)
        due_date_entry.pack()

        tk.Label(add_credit_window, text="Type Sno. of the credit :",bg='#1B2838',fg='white',font=('Bahnschrift SemiBold SemiConden',15)).pack()
        Sno_no = tk.Entry(add_credit_window)
        Sno_no.pack()

        def submit_credit():
            global Sno 
            

            amount = float(amount_entry.get())
            due_date = due_date_entry.get()
            Sno = Sno_no.get()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO credits (user_id, amt, due_date, status, no) VALUES (%s, %s, %s, %s, %s)", (username, amount, due_date, "pending", Sno))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Credit added successfully.")
            add_credit_window.destroy()

        tk.Button(add_credit_window, text="Submit", command=submit_credit).pack(pady=15)

    def view_pending_credits():
        pending_window = Toplevel(main_window2.winfo_toplevel())
        pending_window.title("Pending Credits")
        pending_window.geometry("300x300")
        pending_window.configure(bg='#1B2838')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT no, amt, due_date FROM credits WHERE user_id = %s AND status = 'pending' AND due_date >= CURDATE()", (username,))
        credits = cursor.fetchall()
        cursor.close()
        conn.close()

        for credit in credits:
            tk.Label(pending_window, text=f"Sno: {credit[0]} | Amount: {credit[1]:.2f}₹ | Due: {credit[2]}", bg='#1B2838', fg='yellow', font=('Bahnschrift SemiBold SemiConden', 10)).pack()
        tk.Label(pending_window, text="Enter Sno and Due Date to mark as complete:", bg='#1B2838', fg='white', font=('Bahnschrift SemiBold SemiConden', 10)).pack(pady=2)
        tk.Label(pending_window, text="Sno:", bg='#1B2838', fg='white', font=('Bahnschrift SemiBold SemiConden', 10)).pack(pady=2)
        sno_entry = tk.Entry(pending_window)
        sno_entry.pack()
        tk.Label(pending_window, text="Due Date:", bg='#1B2838', fg='white', font=('Bahnschrift SemiBold SemiConden', 10)).pack(pady=2)
        due_date_entry = tk.Entry(pending_window)
        due_date_entry.pack()

        def mark_completed():
            sno = int(sno_entry.get())
            due_date = str(due_date_entry.get())
            conn = get_db_connection()
            cursor = conn.cursor()
            print("username:", username, type(username))
            print("sno:", sno, type(sno))
            print("due_date:", due_date, type(due_date))
            cursor.execute("SELECT amt FROM credits WHERE user_id = %s AND no = %s AND due_date = %s AND status = 'pending'", (str(username), int(sno), str(due_date)))
            result = cursor.fetchone()
            if result is None:
                messagebox.showerror("Error", "No such pending credit found.")
                return
            amount = result[0]
            cursor.execute("UPDATE users SET balance = balance - %s WHERE username = %s", (int(amount), str(username)))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("UPDATE credits SET status = 'completed' WHERE user_id = %s AND no = %s AND due_date = %s", (str(username), int(sno), str(due_date)))
            conn.commit()
            cursor.close()
            conn.close() 
            messagebox.showinfo("Success", "Credit marked as completed and subtracted from balance.")
            pending_window.destroy()
            update_balance_display()


        tk.Button(pending_window, text="Mark as Completed", command=mark_completed, bg='green', font=('Calibri', 10)).pack(pady=15)

    def view_completed_credits():
        completed_window = Toplevel(main_window2)
        completed_window.title("Completed Credits")
        completed_window.geometry("400x400")
        completed_window.configure(bg='#1B2838')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT amt, due_date FROM credits WHERE user_id = %s AND status = 'completed'", (username,))
        credits = cursor.fetchall()
        cursor.close()
        conn.close()

        scroll = tk.Scrollbar(completed_window, bg='#1B2838',)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(completed_window, yscrollcommand=scroll.set, bg='#1B2838', fg='green', font=('fixedsys', 12), )
        listbox.pack(fill=tk.BOTH, expand=1)

        for credit in credits:
            listbox.insert(tk.END, f"Amount: {credit[0]:.2f}₹ | Due: {credit[1]}")

        scroll.config(command=listbox.yview)

    # Manage Finances
    def manage_finances():
        manage_window = Toplevel(main_window2)
        manage_window.title("Manage Finances")
        manage_window.geometry("400x300")
        manage_window.configure(bg='#1B2838')

        d=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\AddExpense.png")
        d1 = d.resize((150, 45))
        d2 = ImageTk.PhotoImage(d1)

        e=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\AddBalance.png")
        e1 = e.resize((150, 45))
        e2 = ImageTk.PhotoImage(e1)

        f=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\ViewBalance.png")
        f1 = f.resize((150, 45))
        f2 = ImageTk.PhotoImage(f1)

        D=tk.Button(manage_window, text="Add Expense", command=add_expense, image=d2, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
        D.image=d2
        D.place(x=135,y=50)
        E=tk.Button(manage_window, text="Add Balance", command=add_balance, image=e2, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
        E.image=e2
        E.place(x=135,y=125)
        F=tk.Button(manage_window, text="View Balance", command=view_balance,image=f2, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
        F.image=f2
        F.place(x=135,y=200)

    def add_expense():
        expense_window = Toplevel(main_window2)
        expense_window.title("Add Expense")
        expense_window.geometry("300x250")
        expense_window.configure(bg='#1B2838')
        
        tk.Label(expense_window, text="Amount:", bg='#1B2838',fg='red',font=('Bahnschrift SemiBold SemiConden',15)).pack()
        amount_entry = tk.Entry(expense_window)
        amount_entry.pack()
        
        tk.Label(expense_window, text="Category:", bg='#1B2838',fg='white',font=('Bahnschrift SemiBold SemiConden',15)).pack()
        category_entry = tk.Entry(expense_window)
        category_entry.pack()

        tk.Label(expense_window, text="Description:", bg='#1B2838',fg='white',font=('Bahnschrift SemiBold SemiConden',15)).pack()
        tk.Label(expense_window, text="(under 20 letters)", bg='#1B2838',fg='white',font=('Bahnschrift SemiBold SemiConden',7)).pack(pady=0)
        description_entry = tk.Entry(expense_window)
        description_entry.pack()

        def submit_expense():
            amount = float(amount_entry.get())
            category = category_entry.get()
            description = description_entry.get()

            # Subtract the expense amount from the user's balance
            conn = get_db_connection()
            cursor = conn.cursor()  
            cursor.execute("UPDATE users SET balance = balance - %s WHERE username = %s", (amount, username))
            conn.commit()
            cursor.close()
            conn.close()    
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions (user_id, date, amount, category, description) VALUES (%s, CURDATE(), %s, %s, %s)", (username, amount, category, description))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Expense added successfully.")
            expense_window.destroy()
            update_balance_display()

        tk.Button(expense_window, text="Submit", command=submit_expense).pack(pady=15)

    def add_balance():
        balance_window = Toplevel(main_window2)
        balance_window.title("Add Balance")
        balance_window.geometry("300x200")
        balance_window.configure(bg='#1B2838')
        
        tk.Label(balance_window, text="Enter Amount to Add:", bg='#1B2838',fg='yellow',font=('Bahnschrift SemiBold SemiConden',15)).pack(expand=True)
        balance_entry = tk.Entry(balance_window)
        balance_entry.pack(expand=True)

        def submit_balance():
            amount = float(balance_entry.get())
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = balance + %s WHERE username = %s", (amount, username))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Balance updated successfully.")
            balance_window.destroy()
            update_balance_display()

        tk.Button(balance_window, text="Submit", command=submit_balance).pack(pady=15)

    def view_balance():
        view_balance_window = Toplevel(main_window2)
        view_balance_window.title("View Balance")
        view_balance_window.geometry("300x200")
        view_balance_window.configure(bg='#1B2838')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))
        balance = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        tk.Label(view_balance_window, text=f"Your current balance is ${balance:.2f}",bg='#1B2838',fg='green',font=('fixedsys',15)).pack(expand=True)

    # About Creators
    def about_creators():
        about_window = Toplevel(main_window2)
        about_window.title("About Our Creators")
        about_window.geometry("400x300")
        about_window.configure(bg='#1B2838')
        tk.Label(about_window, text="Creators:", font=("Papyrus",20), bg='#1B2838',fg='white').pack(side='top',padx=10)
        tk.Label(about_window, text="Chindumadhi\nHemant\nSrihari", font=("Consolas", 14), bg='#1B2838',fg='white').pack(expand='True')

    DE=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\pictures\deco1.png")
    resized_image5 = DE.resize((338, 153))
    DE1 = ImageTk.PhotoImage(resized_image5)
    
    MF=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\ManageFinances.png")
    resized_image1 = MF.resize((150, 55))
    MF1 = ImageTk.PhotoImage(resized_image1)

    MC=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\manageCredits.png")
    resized_image2 = MC.resize((150, 55))
    MC1 = ImageTk.PhotoImage(resized_image2)

    EH=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\ExpenseHistory.png")
    resized_image3 = EH.resize((150, 55))
    EH1 = ImageTk.PhotoImage(resized_image3)

    AB=Image.open(r"C:\Users\user\Documents\VSC\Finance tracking system MAIN\AboutCreators.png")
    resized_image4 = AB.resize((110, 35))
    AB1 = ImageTk.PhotoImage(resized_image4)

    # Place Buttons in Main Window 2
    button1=tk.Button(main_window2, text="Manage Finances", command=manage_finances, image=MF1, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
    button1.image=MF1
    button1.place(relx=0.5, rely=0.5, anchor="center")
    button2=tk.Button(main_window2, text="Manage Credits", command=manage_credits, image=MC1, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
    button2.image=MC1
    button2.pack(side="right", padx=(0,80))
    button3=tk.Button(main_window2, text="Expense History", command=view_expense_history, image=EH1, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
    button3.image=EH1
    button3.pack(side="left", padx=(80,0))
    button4=tk.Button(main_window2, text="About Creators", command=about_creators, image=AB1, bg='#1B2838',relief="flat", borderwidth=0, highlightthickness=0, highlightbackground=main_window2.cget("bg"), activebackground='#1B2838')
    button4.image=AB1
    button4.pack(side="bottom", pady=30)
    deco = tk.Label(main_window2, image=DE1,bg='#1B2838',relief="flat", borderwidth=0)
    deco.place(x=226.5, y=275)
    deco.image=DE1