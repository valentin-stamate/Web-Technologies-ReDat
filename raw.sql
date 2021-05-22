DROP TABLE IF EXISTS user_topics;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR (255) UNIQUE NOT NULL,
    firstname VARCHAR (255) NOT NULL,
    lastname VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL UNIQUE ,
    password VARCHAR (255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    date_created TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE topics (
    id SERIAL,
    name VARCHAR (255) UNIQUE NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE user_topics (
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    UNIQUE (user_id, topic_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);