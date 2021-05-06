from database.connection.connection import execute_sql
from database.util.password_encryption import PasswordEncryption
from database.util.util import current_timestamp


class User:
    def __init__(self, username, firstname, lastname, email, password, user_id=0):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.date_created = current_timestamp()

    def save(self):
        encrypted_password = PasswordEncryption.encrypt_password(self.password, self.date_created)
        self.password = ''

        try:
            execute_sql(f"""INSERT INTO 
                users(username, firstname, lastname, email, password, date_created) 
                VALUES ('{self.username}', '{self.firstname}', '{self.lastname}', '{self.email}', '{encrypted_password}', '{self.date_created}')""")

            print(f"User {self.username} saved")
        except Exception as e:
            print(e)
            return False

        return True

    def __str__(self):
        return f"User {self.user_id, self.username, self.firstname, self.lastname,self.email, self.password, self.date_created}"
