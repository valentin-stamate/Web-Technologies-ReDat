from util.instance.user import User


class UserData:
    def __init__(self, user: User, topics=[]):
        self.user = user
        self.topics = topics
