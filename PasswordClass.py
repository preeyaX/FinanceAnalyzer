"""
PasswordClass: helps manage the setting up of password and login.
Used in Page 1 (SetPasswordPage) and Page 2 (LoginPage).
Functions:
- Ability to encrypt the inputted password
- Ability to retreive the password from database for comparison
- Ability to save the encrypted password to database
- Ability to validate the inputted password
"""


import sqlite3
from tkinter.constants import FALSE, TRUE
import hashlib as h

class Password:

    @classmethod
    def hashPassword(self, password):
        password_bytes = password.encode()
        return (h.sha3_256(password_bytes).hexdigest())

    @classmethod
    def getFromDb(cls, db_path):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        c.execute("SELECT password_itself FROM password_data")

        set_password = c.fetchone()

        connect.commit()
        connect.close()

        return set_password
    
    @classmethod
    def saveToDb(self, db_path, enc_password):
        connect = sqlite3.connect(db_path)
        c = connect.cursor()

        insert_statement = "INSERT INTO password_data (password_itself) VALUES (?)"
        c.execute(insert_statement, (enc_password,))

        connect.commit()
        connect.close()
    
    @classmethod
    def validatePassword(self, password):
        
        # to check whether to return true or false
        count = 0
        # to check for special characters
        special_ch = "'!@#$%^&*()-+?_=,<>/'"
        

        if any(i.isdigit() for i in password) == TRUE:
            count += 1
        if any(i.isalpha() for i in password) == TRUE:
            count += 1
        if any(i in special_ch for i in password) == TRUE:
            count += 1
        

        if count == 3:
            return TRUE
        else:
            return FALSE
