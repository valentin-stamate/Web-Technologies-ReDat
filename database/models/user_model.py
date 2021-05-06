from database.util.password_encryption import PasswordEncryption


class User:
    def __init__(self, username):
        self.username = username
        self.salt = 0
        self.key = 0


user1 = User('Brent')
user2 = User('John')
PasswordEncryption.encrypt_password(user1, 'mypass')
# Should by false
print(PasswordEncryption.verify_password(user1, 'notmypass'))
# Should by true
print(PasswordEncryption.verify_password(user1, 'mypass'))
