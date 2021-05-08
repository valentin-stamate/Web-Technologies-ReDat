import pandas

from server.database.connection.connection import execute_sql
from server.database.models.user_model import User
from server.external_api.reddit_data import get_hot_posts, get_trending_subreddits
from server.external_api.reddit_post import Post

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

user = User(username='ValentinSt', firstname='Valentin', lastname='Stamate', email='stamtevalentin125@gmail.com',
            password='123456789')
user.save()

user = User(username='Lorenzo', firstname='Iphone', lastname='Laurentiu', email='iphonelaurentiu@gmail.com',
            password='123456789')
user.save()

user = User(username='ValentinSt', password='123456789')
if user.login():
    print(user)
else:
    print("Login failed")

user = User(username='Lex', password='123456789')
print(user.is_valid())

posts_list = get_hot_posts('games',10)
data_frame = pandas.DataFrame()
my_post = None
for post in posts_list:
    my_post = Post(post)
    data_frame = data_frame.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'author': post['data']['author'],
        'score': post['data']['score']
    }, ignore_index=True)
print(data_frame)
print(my_post.title)
trending = get_trending_subreddits(10)
data_frame = pandas.DataFrame()
my_post = None
for post in trending:
    my_post = Post(post)
    data_frame = data_frame.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'author': post['data']['author'],
        'score': post['data']['score']
    }, ignore_index=True)
print(data_frame)
# print(post['data'].keys()) #items that can be obtained
