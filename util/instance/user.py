from util.util import current_timestamp


class User:
    def __init__(self, username, firstname='DummyUser', lastname='DummyUser', email='dummyuser@gmail.com',
                 password='123456789', user_id=0, image_url='https://i.postimg.cc/RF11Kn7j/default.png', date_created=current_timestamp()):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.image_url = image_url
        self.date_created = date_created
