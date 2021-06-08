from services.server.database.connection.connection import execute_sql
from util.password_encryption import PasswordEncryption
from util.util import current_timestamp
from util.validation.validation import valid_username, valid_name, valid_email, valid_password


class UserModel:
    def __init__(self, username, firstname='DummyUser', lastname='DummyUser', email='dummyuser@gmail.com',
                 password='123456789', user_id=0, image_url='https://i.postimg.cc/RF11Kn7j/default.png',
                 date_created=current_timestamp()):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.image_url = image_url
        self.date_created = date_created

    # CRUD OPERATIONS
    def save(self):
        encrypted_password = PasswordEncryption.encrypt_password(self.password, self.date_created)
        self.password = ''

        db_user = UserModel.get_by_username(self.username)['object']

        if db_user is not None:
            return {'status': False, 'message': 'User already exists'}

        db_user = UserModel.__get_user_by_key('email', f"'{self.email}'")['object']

        if db_user is not None:
            return {'status': False, 'message': 'Email already taken'}

        try:
            execute_sql(f"""INSERT INTO 
                users(username, firstname, lastname, email, password, image_url, date_created) 
                VALUES 
                ('{self.username}', '{self.firstname}', '{self.lastname}', '{self.email}', 
                '{encrypted_password}', '{self.image_url}', '{self.date_created}')""")

            print(f"User {self.username} saved")
        except Exception as e:
            print(e)
            return {'status': False, 'message': 'Error at adding user'}

        self.get_user_id()

        return {'status': True, 'message': 'User created successfully'}

    def update(self):
        if self.user_id == 0:
            return {'status': False, 'message': 'User should be logged first'}

        execute_sql(
            f"UPDATE users SET username = '{self.username}', firstname = '{self.firstname}', image_url = '{self.image_url}', lastname = '{self.lastname}', password = '{self.password}', email = '{self.email}' WHERE id = {self.user_id}")

        return {'status': True, 'message': 'User updated successfully'}

    def delete(self) -> bool:
        try:
            execute_sql(f"DELETE FROM users WHERE id = {self.user_id}")
            return True
        except Exception as e:
            return False

    # AUTHENTICATION
    def login(self) -> dict:

        db_user = UserModel.get_by_username(self.username)['object']

        if db_user is None:
            return {'status': False, 'message': "User doesn't exist"}

        if db_user.password == PasswordEncryption.encrypt_password(self.password, db_user.date_created):
            self.user_id = db_user.user_id
            self.username = db_user.username
            self.firstname = db_user.firstname
            self.lastname = db_user.lastname
            self.email = db_user.email
            self.password = ''
            self.date_created = db_user.date_created
            return {'status': True, 'message': 'Login success'}

        return {'status': False, 'message': 'Incorrect password'}

    # VALIDATION
    def is_valid(self):
        if not valid_username(self.username):
            return {'status': False, 'message': 'Invalid username'}

        if not valid_name(self.firstname):
            return {'status': False, 'message': 'Invalid firstname'}

        if not valid_name(self.lastname):
            return {'status': False, 'message': 'Invalid lastname'}

        if not valid_email(self.email):
            return {'status': False, 'message': 'Invalid email'}

        if not valid_password(self.password):
            return {'status': False, 'message': 'Invalid password'}

        return {'status': True, 'message': 'Invalid email'}

    # GETTERS
    @staticmethod
    def get_by_username(username) -> {}:
        return UserModel.__get_user_by_key("username", f"'{username}'")

    @staticmethod
    def get_by_id(user_id) -> {}:
        return UserModel.__get_user_by_key("id", f"{user_id}")

    def get_user_id(self):
        self.user_id = UserModel.__get_user_by_key('username', f"'{self.username}'")['object'].user_id

    @staticmethod
    def __get_user_by_key(key, value) -> {}:
        try:
            row = execute_sql(f"SELECT * FROM users WHERE {key} = {value}")[0]
            user = UserModel(user_id=row[0], username=row[1], firstname=row[2], lastname=row[3],
                             email=row[4], password=row[5], image_url=row[6], date_created=row[7])
            return {'object': user, 'message': 'Success'}
        except IndexError:
            return {'object': None, 'message': f"User with key:{key} and value:{value} not found"}

    def __str__(self):
        return f"User {self.user_id, self.username, self.firstname, self.lastname, self.email, self.password, self.image_url, self.date_created}"
