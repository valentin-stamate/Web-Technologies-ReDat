import typing

from services.server.database.connection.connection import execute_sql
from services.server.database.models.topic_model import TopicModel
from services.server.database.models.user_model import UserModel


class UserTopicModel:
    def __init__(self, user_model: UserModel, topic_model: TopicModel = None):
        self.user_model = user_model
        self.topic_model = topic_model

    # CRUD OPERATIONS
    def save(self):
        try:
            execute_sql(f"""INSERT INTO user_topics(user_id, topic_id) 
            VALUES ({self.user_model.user_id}, {self.topic_model.topic_id})""")

            print(f"User Topic {self.user_model.username} -> {self.topic_model.name} saved")
        except Exception as e:
            print(e)
            return {'status': False, 'message': 'Error at adding topic to user'}

        return {'status': True, 'message': 'User created successfully'}

    def delete(self) -> bool:
        try:
            execute_sql(f'''DELETE FROM user_topics WHERE 
                            user_id = {self.user_model.user_id} AND topic_id = {self.topic_model.topic_id}''')
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_topic_from_users(topic_model: TopicModel) -> bool:
        try:
            execute_sql(f"DELETE FROM user_topics WHERE topic_id = {topic_model.topic_id}")
            return True
        except Exception as e:
            return False

    # GETTERS

    @staticmethod
    def get_all(user_model: UserModel) -> typing.List['TopicModel']:
        topics = []

        rows = execute_sql(f"SELECT t.id, t.name FROM topics t JOIN user_topics ut "
                           f"ON t.id = ut.topic_id AND user_id = {user_model.user_id}")

        for row in rows:
            topics.append(TopicModel(topic_id=row[0], name=row[1]))

        return topics

    @staticmethod
    def delete_user_topics(user_model: UserModel) -> bool:
        execute_sql(f"DELETE FROM user_topics WHERE user_id = {user_model.user_id}")
        return True

    def __str__(self):
        return f"User Topic {self.user_model.username} -> {self.topic_model.name}"

