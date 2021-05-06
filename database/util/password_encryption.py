import hashlib


class PasswordEncryption:

    @staticmethod
    def encrypt_password(password, date_created):
        # salt = os.urandom(32)  # A random salt for this user
        salt = abs(hash(date_created)).to_bytes(16, 'big')

        encoded_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        return str(encoded_password)[2:len(encoded_password) - 2]
