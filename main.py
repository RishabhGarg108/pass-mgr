from database import PasswordDB
from crypto import encrypt, decrypt
from password_generator import generateRandomPassword
from authenticate import authenticatePassword, authenticateFace

import pyperclip  # For using clipboard
from decouple import config  # For storing environment variables
from texttable import Texttable  # For clearing beautiful tables

# Extracting the environment variables.
SECRET_KEY = config('SECURITY_KEY')
AUTHENTICATION_TYPE = config('AUTHENTICATION_TYPE')

# Initializing database.
db = PasswordDB()

def accessPassword():
    print('Enter the name of the website.')
    website = input(">>>")
    print('Enter the email.')
    email = input(">>>")

    password = db.getPassword(website, email)
    if(len(password) == 0):
        print("Password does not exist.")
    else:
        password = decrypt(SECRET_KEY, password[0][0])
        pyperclip.copy(password)
        print("Your password is copied to clipboard!")

def savePassword():
    print('Enter the name of the website.')
    website = input(">>>")
    print('Enter the user name.')
    user_name = input(">>>")
    print('Enter the email.')
    email = input(">>>")

    print("For creating a system generated strong random password, enter 'y' or 'n'")
    is_random_pass = input(">>>")
    if is_random_pass == 'y':
        password = generateRandomPassword()
    else:
        print("Enter your own password.")
        password = input(">>>")
    
    password = encrypt(SECRET_KEY, password)

    db.savePassword(website, user_name, email, password)

def deletePassword():
    print('Enter the name of the website.')
    website = input(">>>")
    print('Enter the email.')
    email = input(">>>")

    db.deletePassword(website, email)

# Displays all the saved passwords.
def showAllPasswords():
    records = db.showAllPasswords()
    
    table = Texttable()
    table.add_rows([["Website", "User Name", "Email"]] + records)
    print(table.draw())

# Display the available commands table.
def showCommands():
    table = Texttable()
    table.add_rows([["Command", "Function"],
                    ["cmd", "Display this box of available commands."],
                    ["get", "Access a saved password."],
                    ["save", "Save a new password."],
                    ["del", "Delete an existing password."],
                    ["all", "Show all saved passwords."],
                    ["exit()", "Exit the program."]])

    print(table.draw())
    

def cli():
    print("Welcome to the command-line interface of Pass-Mgr.")
    print("I am a locker that will safely store all your passwords.\n")

    auth = False
    if AUTHENTICATION_TYPE == '1':
        print("To access saved passwords or save new password, enter the root password.")
        auth = authenticatePassword()
    if AUTHENTICATION_TYPE == '2':
        print('Authenticating Face.')
        auth = authenticateFace()

    if(auth):
        print("\n\n\t\tAccess granted!")
    else:
        print("Invalid authentication.")
        exit()

    showCommands()

    command = "dummy"
    while command != "exit()":
        command = input(">>>").lower()
        if command == "get":
            accessPassword()
        elif command == "save":
            savePassword()
        elif command == "del":
            deletePassword()
        elif command == "all":
            showAllPasswords()
        elif command == "cmd":
            showCommands()
        elif command == "exit()":
            pass
        else:
            print("Enter a valid command")
    exit()


if __name__ == "__main__":
    cli()
