from database.connection.connection import execute_sql
import datetime
import time


def current_timestamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


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

execute_sql(f"""INSERT INTO 
    users(username, firstname, lastname, email, password, date_created) 
    VALUES ('ValentinSt', 'Valentin', 'Stamate', 'stamatevalentin125@gmail.com', '12345678', '{current_timestamp()}')"""
)


