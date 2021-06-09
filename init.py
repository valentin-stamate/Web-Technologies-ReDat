from services.server.database.connection.connection import execute_sql
from services.server.database.models.topic_model import TopicModel
from services.server.database.models.user_model import UserModel
from services.server.database.models.user_topics_model import UserTopicModel
from util.external.initial_topics import topics

execute_sql('''DROP TABLE IF EXISTS user_topics''')
execute_sql('''DROP TABLE IF EXISTS topics''')
execute_sql('''DROP TABLE IF EXISTS users''')

execute_sql('''CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR (255) UNIQUE NOT NULL,
    firstname VARCHAR (255) NOT NULL,
    lastname VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL UNIQUE ,
    password VARCHAR (255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    date_created TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
)''')
print("Table users created successfully")

execute_sql('''CREATE TABLE topics (
    id SERIAL,
    name VARCHAR (255) UNIQUE NOT NULL,
    url VARCHAR (255) UNIQUE NOT NULL,
    PRIMARY KEY (id)
)''')
print("Table topics created successfully")

execute_sql('''CREATE TABLE user_topics (
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    UNIQUE (user_id, topic_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
)''')
print("Table user_topics created successfully")


def create_users():
    UserModel(username='ValentinSt', firstname='Valentin', lastname='Stamate', email='stamtevalentin125@gmail.com',
              password='123456789', is_admin=True).save()

    UserModel(username='Lorenzo112', firstname='Iphone', lastname='Laurentiu', email='iphonelaurentiu@gmail.com',
              password='123456789').save()


def insert_topics():
    for topic in topics:
        topic_model = TopicModel(topic)
        topic_model.save()


def add_user_topics():
    user_model: UserModel = UserModel.get_by_username('ValentinSt')['object']

    for i in range(1, 5):
        topic_model = TopicModel.get_by_id(i)['object']
        user_topic = UserTopicModel(user_model, topic_model)
        user_topic.save()


create_users()
insert_topics()
add_user_topics()

