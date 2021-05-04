import hashlib
import os


class PasswordEncryption:

    @staticmethod
    def encrypt_password(user, password):
        salt = os.urandom(32)  # A random salt for this user
        user.salt = salt
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user.salt, 100000)
        user.password = key

    @staticmethod
    def verify_password(user, password):
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user.salt, 100000)
        return user.password == new_key
