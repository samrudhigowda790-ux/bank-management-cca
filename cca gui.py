import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------------- FILE LOCATION ----------------
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank_data.json")

# ---------------- DATA HANDLING ----------------
def load_data():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_data():
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save data:\n{e}")

data = load_data()

# ---------------- SECURITY ----------------
attempts = 3

def check_password(acc):
    global attempts

    pwd = pass_entry.get().strip()

    if pwd == "":
        messagebox.showerror("Error", "Enter password!")
        return False

    if pwd == data[acc]["password"]:
        attempts = 3
        return True

    attempts -= 1

    if attempts <= 0:
        messagebox.showerror(
            "Blocked",
            "FAILED!\nAttempts are over."
        )
        attempts = 3
        clear_entries()
        return False

    messagebox.showerror(
        "Wrong Password",
        f"Incorrect password.\nAttempts left: {attempts}"
    )
    return False

# ---------------- UTILITIES ----------------
def clear_entries():
    acc_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def get_account():
    acc = acc_entry.get().strip()

    if acc == "":
        messagebox.showerror("Error", "Enter account number!")
        return None

    if acc not in data:
        messagebox.showerror("Error", "Account not found!")
        return None

    return acc

# ---------------- ACCOUNT CREATION ----------------
def create_account():
    acc = acc_entry.get().strip()
    name = name_entry.get().strip()
    pwd = pass_entry.get().strip()

    if not acc or not name or not pwd:
        messagebox.showerror("Error", "Fill all required fields!")
        return

    if not acc.isdigit():
        messagebox.showerror("Error", "Account number must be numeric!")
        return

    if len(pwd) != 4 or not pwd.isdigit():
        messagebox.showerror("Error", "Password must be exactly 4 digits!")
        return

    if acc in data:
        messagebox.showerror("Error", "Account already exists!")
        return

    data[acc] = {
        "name": name,
        "password": pwd,
        "balance": 0.0,
        "transactions": []
    }

    save_data()

    messagebox.showinfo(
        "Success",
        "Account created successfully!"
    )

    clear_entries()

# ---------------- DEPOSIT ----------------
def deposit():
    acc = get_account()

    if not acc:
        return

    if not check_password(acc):
        return

    try:
        amt = float(amount_entry.get())

        if amt <= 0:
            raise ValueError

        data[acc]["balance"] += amt
        data[acc]["transactions"].append(f"Deposited ₹{amt}")

        save_data()

        messagebox.showinfo(
            "Success",
            f"₹{amt} deposited successfully!"
        )

        clear_entries()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid amount!"
        )

# ---------------- WITHDRAW ----------------
def withdraw():
    acc = get_account()

    if not acc:
        return

    if not check_password(acc):
        return

    try:
        amt = float(amount_entry.get())

        if amt <= 0:
            raise ValueError

        if amt > data[acc]["balance"]:
             current_balance = data[acc]["balance"]
             
             messagebox.showerror(
                "Insufficient Balance",
                f"Requested Amount: ₹{amt}\n"
                f"Available Balance: ₹{current_balance}\n\n"
                "Please enter a smaller amount."
            )
        return

        data[acc]["balance"] -= amt
        data[acc]["transactions"].append(f"Withdrawn ₹{amt}")

        save_data()

        messagebox.showinfo(
            "Success",
            f"₹{amt} withdrawn successfully!"
        )

        clear_entries()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid amount!"
        )

# ---------------- BALANCE ----------------
def balance():
    acc = get_account()

    if not acc:
        return

    if not check_password(acc):
        return

    messagebox.showinfo(
        "Balance Enquiry",
        f"Account Holder: {data[acc]['name']}\n\nBalance: ₹{data[acc]['balance']}"
    )

# ---------------- MINI STATEMENT ----------------
def mini_statement():
    acc = get_account()

    if not acc:
        return

    if not check_password(acc):
        return

    transactions = data[acc]["transactions"]

    if len(transactions) == 0:
        statement = "No transactions available."
    else:
        statement = "\n".join(transactions[-5:])

    messagebox.showinfo(
        "Mini Statement",
        statement
    )

# ---------------- EXIT ----------------
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Banking System")
root.geometry("500x600")
root.configure(bg="black")
root.resizable(False, False)

# Title
title = tk.Label(
    root,
    text="BANKING SYSTEM",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="black"
)
title.pack(pady=20)

# Labels & Entries
tk.Label(root, text="Account Number", fg="white", bg="black").pack()
acc_entry = tk.Entry(root, width=30)
acc_entry.pack(pady=5)

tk.Label(root, text="Name (Create Only)", fg="white", bg="black").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Label(root, text="4-Digit Password", fg="white", bg="black").pack()
pass_entry = tk.Entry(root, show="*", width=30)
pass_entry.pack(pady=5)

tk.Label(root, text="Amount", fg="white", bg="black").pack()
amount_entry = tk.Entry(root, width=30)
amount_entry.pack(pady=5)

# Button Frame
frame = tk.Frame(root, bg="black")
frame.pack(pady=20)

button_width = 15

tk.Button(
    frame,
    text="Create",
    bg="skyblue",
    width=button_width,
    command=create_account
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    frame,
    text="Deposit",
    bg="green",
    fg="white",
    width=button_width,
    command=deposit
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    frame,
    text="Withdraw",
    bg="red",
    fg="white",
    width=button_width,
    command=withdraw
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    frame,
    text="Balance",
    bg="white",
    width=button_width,
    command=balance
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    frame,
    text="Mini Statement",
    bg="white",
    width=button_width,
    command=mini_statement
).grid(row=2, column=0, padx=5, pady=5)

tk.Button(
    frame,
    text="Clear",
    bg="white",
    width=button_width,
    command=clear_entries
).grid(row=2, column=1, padx=5, pady=5)

tk.Button(
    root,
    text="EXIT",
    bg="brown",
    fg="white",
    width=25,
    command=exit_app
).pack(pady=20)

root.mainloop()
