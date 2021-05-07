import hashlib


class PasswordEncryption:

    @staticmethod
    def encrypt_password(password, date_created):
        password += str(date_created)
        return str(hashlib.sha256(password.encode()).hexdigest())
