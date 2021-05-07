import re

from database.connection.connection import execute_sql
from database.util.password_encryption import PasswordEncryption
from database.util.util import current_timestamp


class User:
    def __init__(self, username, firstname='DummyUser', lastname='DummyUser', email='dummyuser@gmail.com',
                 password='123456789', user_id=0, date_created=''):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.date_created = current_timestamp()

    # CRUD OPERATIONS
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

        self.get_user_id()

        return True

    def update(self):
        if self.user_id == 0:
            print("User should be saved or logged first")
            return False

        execute_sql(
            f"UPDATE users SET username = '{self.username}', firstname = '{self.firstname}', lastname = '{self.lastname}', password = '{self.password}' WHERE id = {self.user_id}")

        return True

    @staticmethod
    def __get_user_by_key(key, value):
        try:
            row = execute_sql(f"SELECT * FROM users WHERE {key} = {value}")[0]
            return User(user_id=row[0], username=row[1], firstname=row[2], lastname=row[3],
                        email=row[4], password=row[5], date_created=row[6])
        except IndexError:
            print(f"User with key:{key} and value:{value} not found")
            return None

    # AUTHENTICATION
    def login(self):

        db_user = User.get_by_username(self.username)

        if db_user is None:
            return False

        if db_user.password == PasswordEncryption.encrypt_password(self.password, db_user.date_created):
            self.user_id = db_user.user_id
            self.username = db_user.username
            self.firstname = db_user.firstname
            self.lastname = db_user.lastname
            self.email = db_user.email
            self.password = ''
            self.date_created = db_user.date_created
            return True

        return False

    # VALIDATION
    def is_valid(self):
        if len(self.username) < 3:
            return False

        if len(self.firstname) < 8:
            return False

        if len(self.lastname) < 8:
            return False

        email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        if not re.search(email_regex, self.email):
            return False

        if len(self.password) < 8:
            return False

        return True

    # GETTERS
    @staticmethod
    def get_by_username(username):
        return User.__get_user_by_key("username", f"'{username}'")

    @staticmethod
    def get_by_id(user_id):
        return User.__get_user_by_key("id", f"{user_id}")

    def get_user_id(self):
        self.user_id = User.__get_user_by_key('username', f"'{self.username}'").user_id

    def __str__(self):
        return f"User {self.user_id, self.username, self.firstname, self.lastname, self.email, self.password, self.date_created}"
