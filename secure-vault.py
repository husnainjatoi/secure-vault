from cryptography.fernet import Fernet
import os 
import random
import string

letters = list(string.ascii_letters)
numbers = list(string.digits)
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def writekey():
    if os.path.exists('key.key'):
        return
    key = Fernet.generate_key()
    with open('key.key', 'wb') as keyFile:
        keyFile.write(key)


def loadkey():
    with open('key.key', 'rb') as file:
        key = file.read()
    return key


writekey()
key = loadkey() 
fer = Fernet(key)


def menu():
    print("\nMenu:")
    print("1. View passwords\n2. Add new passwords\n3. Generate random password" \
    "\n4. Manage accounts\n5. Change master password\n6. Exit")


def view():
    if os.path.exists('password_manager.txt'):
        with open('password_manager.txt', 'r') as file:

            if not file.read(1):
                print("No records saved yet.")
                return
            file.seek(0)

            for line in file:
                line = line.split('|')
                account_name = line[0].strip()
                password = line[1].strip()
                print(f"Account Name: {account_name} | Password: {fer.decrypt(password.encode()).decode()}")
    else:
        print("No records found.")


def add():
    account_name = input("Enter Account Name: ").strip()
    if len(account_name) <= 0:
        print("Error: Account name cannot be empty.")
        return
    password = input(f"Enter the password for '{account_name}': ")
    if len(password) <= 0:
        print("Error: Password cannot be empty.")
        return

    with open('password_manager.txt', 'a') as file:
        file.write(f"{account_name}|{fer.encrypt(password.encode()).decode()}\n")   
        print(f"'{account_name}' added successfully!")  


def masterPassword():
    while True:
        if os.path.exists('master_pwd.key'):

            with open('master_pwd.key', 'rb') as file:

                master_pwd = fer.decrypt(file.read())
                userpwd = input("Enter the master password: ").strip()

                if userpwd != master_pwd.decode():
                    print("Incorrect master password. Please try again.")
                else:
                    break

        else:
            while True:
                master_pwd = input("Set a new master password: ").strip()
                if len(master_pwd) <= 0:
                    print("Error! No input received. Please try again.")
                else:
                    with open('master_pwd.key', 'wb') as file:
                        file.write(fer.encrypt(master_pwd.encode()))
                    break


def change_masterpwd():
    consent = input("Are you sure you want to change your master password? (y/n): ").lower().strip()
    if consent == 'yes' or consent == 'y':
        with open('master_pwd.key', 'rb') as file:
            oldpass = input("Please enter your current password to continue: ").strip()
            masterpass = fer.decrypt(file.read())

            if len(oldpass) <= 0:
                print("Error! No input received. Please try again.")
                return
            if oldpass != masterpass.decode():
                print("Incorrect Password!")
                return
        
        master_pwd = input("Set a new master password: ").strip()

        if len(master_pwd) <= 0:
            print("Error! No input received. Please try again.")
            return
        if master_pwd == oldpass:
            print("New password must be different from the current one.")
            return
            
        with open('master_pwd.key', 'wb') as file:
            file.write(fer.encrypt(master_pwd.encode()))
            print("Password changed successfully!")  


def change_account_name():
    updated_lines = []
    found = False
    account_name = input("Please enter the current account name to update: ").strip()
    if len(account_name) <= 0:
        print("Error! No input received. Please try again.")
        return
    
    with open('password_manager.txt', "r") as file:
        lines = file.readlines()
              
    for line in lines:
        if line.startswith(account_name + '|'):
            pieces = line.split('|')
            passw = fer.decrypt(pieces[1].strip().encode()).decode()
            new_name = input("Enter the new account name: ").strip()
            old_name = pieces[0]
            
            if new_name == old_name:
                print("New account name must be different from the current one.")
                return
            if len(new_name) <= 0:
                print("Error! No input received. Please try again.")
                return
            
            updated_lines.append(f"{new_name}|{fer.encrypt(passw.encode()).decode()}\n")
            print("\nAccount name changed successfully!")
            found = True
        else:
            updated_lines.append(line)
    if not found:
        print("No such account found in records.")
        return
    with open('password_manager.txt', 'w') as file:
        for line in updated_lines:
            file.write(line)



def change_account_password():
    updated_lines = []
    found = False
    account_name = input("Please enter the account name to update its password: ").strip()
    if len(account_name) <= 0:
        print("Error! No input received. Please try again.")
        return
    
    with open('password_manager.txt', "r") as file:
        lines = file.readlines()
              
    for line in lines:
        if line.startswith(account_name + '|'):
            pieces = line.split('|')
            new_pass = input("Enter the new password: ").strip()
            old_pass = fer.decrypt(pieces[1].strip().encode()).decode()
            if new_pass == old_pass:
                print("New password must be different from the current one.")
                return
            if len(new_pass) <= 0:
                print("Error! New password must be different from the current one.")
                return
            
            updated_lines.append(f"{account_name}|{fer.encrypt(new_pass.encode()).decode()}\n")
            print("\nAccount password changed successfully!")
            found = True
        else:
            updated_lines.append(line)
    
    if not found:
        print("No such account found in records.")
        return
    with open('password_manager.txt', 'w') as file:
        for line in updated_lines:
            file.write(line)


def delete_account():
    updated_lines = []
    deleted = False
    account_name = input("Enter the name of the account you want to delete: ").strip()
    if len(account_name) <=0:
        print("Error! No input received. Please try again.")
        return
    
    with open('password_manager.txt', 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.startswith(account_name + '|'):
            deleted = True
            continue
        else:
            updated_lines.append(line)
        
    if deleted:
        print(f"\nAccount {account_name} deleted successfully!")
    else:
        print("No such account found in records.")
    
    with open('password_manager.txt', 'w') as file:
        for line in updated_lines:
            file.write(line)


def manage_accounts():
    print("Manage accounts:\n1. Change Account Name\n2. Change Password\n3. Delete an entry")

    try:
        choice = int(input().strip())
        print("")
    except ValueError:
        print("Invalid Choice!")
        return
    
    if choice == 1:
        change_account_name()

    elif choice == 2:
        change_account_password()

    elif choice == 3:
        delete_account()

    else:
        print("Invalid Choice!")
        return


def random_password():
    try:
        num_letters= int(input("How many letters would you like in your password?\n").strip()) 
    except ValueError:
        print("Error! Please enter an integer")
        return
    try:
        num_symbols = int(input("How many symbols would you like?\n").strip())
    except ValueError:
        print("Error! Please enter an integer")
        return
    try:
        num_numbers = int(input("How many numbers would you like?\n").strip())
    except ValueError:
        print("Error! Please enter an integer")
        return

    password_list = []
    for char in range(1, num_letters+1):
        password_list.append(random.choice(letters))

    for num in range(1, num_numbers+1):
        password_list.append(random.choice(numbers))

    for sym in range(1, num_symbols+1):
        password_list.append(random.choice(symbols))

    random.shuffle(password_list)

    password = ''
    for char in password_list:
        password += char

    print("\nYour randomly generated password is:", password)


masterPassword()
print("Welcome to the password manager!")

while True:
    menu()

    try:
        choice = int(input().strip())
        print("")
    except ValueError:
        print("Please enter a number (1-6).")
        continue
    
    if choice == 1:
        view()
    elif choice == 2:
        add()
    elif choice == 3:
        random_password()
    elif choice == 4:
        manage_accounts()
    elif choice == 5:
        change_masterpwd()
    elif choice == 6:
        print("Thank you for using the password manager.")
        exit()
    else:
        print("Invalid Choice!")
        continue
