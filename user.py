from password_encryption import PasswordEncryption


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


user1 = User('Brent', 'mypassword')
user2 = User('John', 'otherpass')
PasswordEncryption.add_user(PasswordEncryption, user1)

# Verification attempt 1 (incorrect password)
print(PasswordEncryption.verify_password(PasswordEncryption, user1))

# Verification attempt 2 (correct password)
print(PasswordEncryption.verify_password(PasswordEncryption, user2))

# Adding a different user
PasswordEncryption.add_user(PasswordEncryption, user2)
print(PasswordEncryption.verify_password(PasswordEncryption, user2));

# The keys are the same thus the passwords were the same for this user also
