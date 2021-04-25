import hashlib
import os


class PasswordEncryption:

    @staticmethod
    def encrypt_password(user, password):
        salt = os.urandom(32)  # A new salt for this user
        user.salt = salt;
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        user.key = key

    @staticmethod
    def verify_password(user, password):
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user.salt, 100000)
        return user.key == new_key  # The keys are not the same thus the passwords were not the same
