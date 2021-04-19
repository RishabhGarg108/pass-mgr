import sqlite3
from crypto import encrypt, decrypt


class PasswordDB:
    def __init__(self):
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute('''CREATE TABLE passwords
                        (website, user_name, email, password)''')
        except(Exception) as error:
            pass

    def savePassword(self, website, user_name, email, password):
        records = self.cursor.execute(f"SELECT * FROM passwords WHERE website = '{website}' AND email = '{email}'")

        if(len([record for record in records]) > 0):
            print("A password already exixts. So, overwriting it.")
            self.cursor.execute(f"UPDATE passwords SET password = '{password}' WHERE  website = '{website}' AND email = '{email}'")
        else:
            
            self.cursor.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)",
                        (website, user_name, email, password))
            print("New password saved sucessfully.")

        self.connection.commit()

    def deletePassword(self, website, email):
        self.cursor.execute(f"DELETE FROM passwords WHERE website = '{website}' AND email = '{email}'")
        self.connection.commit()
        print("Password deleted successfully.")

    def getPassword(self, website, email):
        password = self.cursor.execute(f"SELECT password FROM passwords WHERE website = '{website}' AND email = '{email}'")
        password = [i for i in password]
        return password

    def showAllPasswords(self):
        records = self.cursor.execute("SELECT * FROM passwords")
        records = [i[:3] for i in records]
        
        return records

    def __del__(self):
        self.connection.close()

