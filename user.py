from password_encryption import PasswordEncryption


class User:
    def __init__(self, username, date):
        self.username = username
        self.password = ''
        self.salt = ''
        self.creation_date_and_time = date

    def __str__(self):
        return 'username = {self.username}\n' \
               'password = {self.password}\n' \
               'salt = {self.salt}\n' \
               'creation date = {self.creation_date_and_time}\n' \
            .format(self=self)

