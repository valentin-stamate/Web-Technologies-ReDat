from database.connection.connection import execute_sql
from database.models.user_model import User

execute_sql('''CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR (255) UNIQUE NOT NULL,
    firstname VARCHAR (255) NOT NULL,
    lastname VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL UNIQUE ,
    password VARCHAR (255) NOT NULL,
    date_created TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
)''')
print("Table users created successfully")

user = User(username='ValentinSt', firstname='Valentin', lastname='Stamate', email='stamtevalentin125@gmail.com', password='123456789')
user.save()

user = User(username='Lorenzo', firstname='Iphone', lastname='Laurentiu', email='iphonelaurentiu@gmail.com', password='123456789')
user.save()

user.username = "kjdaskdsa"

user.update()




