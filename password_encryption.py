import hashlib
import os


class PasswordEncryption:
    users = {}

    @staticmethod
    def add_user(self, user):
        salt = os.urandom(32)  # A new salt for this user
        key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)
        self.users[user.username] = {'salt': salt, 'key': key}

    @staticmethod
    def verify_password(self, user):
        salt = self.users[user.username]['salt']  # Get the salt
        key = self.users[user.username]['key']  # Get the correct key
        new_key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000)

        return key == new_key  # The keys are not the same thus the passwords were not the same
