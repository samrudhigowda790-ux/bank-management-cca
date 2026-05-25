import json

FILE = "bank_data.json"

# ---------------- FILE HANDLING ----------------
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------------- FUNCTIONS ----------------

def create_account():
    try:
        acc = input("Enter Account Number: ")

        if acc in data:
            print("Account already exists!\n")
            return

        name = input("Enter Name: ")

        data[acc] = {
            "name": name,
            "balance": 0,
            "transactions": []
        }

        save_data(data)
        print("Account created successfully!\n")

    except Exception as e:
        print("Error:", e)


def deposit():
    try:
        acc = input("Enter Account Number: ")

        if acc not in data:
            print("Account not found!\n")
            return

        amount = float(input("Enter deposit amount: "))

        if amount <= 0:
            print("Invalid amount!\n")
            return

        data[acc]["balance"] += amount
        data[acc]["transactions"].append(f"Deposited: {amount}")

        save_data(data)
        print("Deposit successful!\n")

    except ValueError:
        print("Enter valid numeric amount!\n")


def withdraw():
    try:
        acc = input("Enter Account Number: ")

        if acc not in data:
            print("Account not found!\n")
            return

        amount = float(input("Enter withdrawal amount: "))

        if amount <= 0:
            print("Invalid amount!\n")
            return

        if data[acc]["balance"] < amount:
            print("Insufficient balance!\n")
            return

        data[acc]["balance"] -= amount
        data[acc]["transactions"].append(f"Withdrawn: {amount}")

        save_data(data)
        print("Withdrawal successful!\n")

    except ValueError:
        print("Enter valid numeric amount!\n")


def balance_enquiry():
    try:
        acc = input("Enter Account Number: ")

        if acc not in data:
            print("Account not found!\n")
            return

        print("Name:", data[acc]["name"])
        print("Balance:", data[acc]["balance"], "\n")

    except Exception as e:
        print("Error:", e)


def mini_statement():
    try:
        acc = input("Enter Account Number: ")

        if acc not in data:
            print("Account not found!\n")
            return

        print("\n--- MINI STATEMENT ---")
        print("Name:", data[acc]["name"])
        print("Last Transactions:")

        transactions = data[acc]["transactions"]

        if not transactions:
            print("No transactions yet.\n")
        else:
            for t in transactions[-5:]:
                print("-", t)

        print()

    except Exception as e:
        print("Error:", e)


# ---------------- MAIN MENU ----------------

while True:
    print("===== BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Balance Enquiry")
    print("5. Mini Statement")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        deposit()

    elif choice == "3":
        withdraw()

    elif choice == "4":
        balance_enquiry()

    elif choice == "5":
        mini_statement()

    elif choice == "6":
        print("Thank you for using Banking System!")
        break

    else:
        print("Invalid choice! Try again.\n")
