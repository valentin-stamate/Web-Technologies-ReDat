from services.server.database.connection.connection import execute_sql
from services.server.database.models.user_model import UserModel

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
    date_created TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
)''')
print("Table users created successfully")

execute_sql('''CREATE TABLE topics (
    id SERIAL,
    name VARCHAR (255) UNIQUE NOT NULL,
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

user = UserModel(username='ValentinSt', firstname='Valentin', lastname='Stamate', email='stamtevalentin125@gmail.com',
                 password='123456789')
user.save()

user = UserModel(username='Lorenzo', firstname='Iphone', lastname='Laurentiu', email='iphonelaurentiu@gmail.com',
                 password='123456789')
user.save()
