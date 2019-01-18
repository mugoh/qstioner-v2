"""
    This module contains the database queries used in the application models
"""

CREATE_TABLE_USERS = """
    CREATE TABLE IF NOT EXISTS USERS (
    ID SERIAL PRIMARY KEY NOT NULL,
    FIRSTNAME VARCHAR(60) NOT NULL,
    LASTNAME VARCHAR(60) NOT NULL,
    OTHERNAME VARCHAR(50),
    EMAIL VARCHAR(40) UNIQUE NOT NULL,
    PHONENUMBER INTEGER NOT NULL,
    USERNAME VARCHAR(30) UNIQUE NOT NULL,
    ISADMIN BOOLEAN DEFAULT FALSE,
    PASSWORD VARCHAR NOT NULL

    );
"""

CREATE_TABLE_MEETUPS = """
    CREATE TABLE IF NOT EXISTS MEETUPS (
    ID SERIAL PRIMARY KEY NOT NULL,
    TOPIC VARCHAR(112) NOT NULL,
    IMAGES VARCHAR(1024)[],
    LOCATION VARCHAR(50) NOT NULL,
    HAPPENING_ON TEXT NOT NULL,
    TAGS TEXT []
    );
"""

CREATE_TABLE_QUESTIONS = """
    CREATE TABLE IF NOT EXISTS QUESTIONS (
    ID SERIAL PRIMARY KEY NOT NULL,
    TITLE VARCHAR(40) NOT NULL,
    BODY VARCHAR(40) NOT NULL,
    MEETUP INTEGER REFERENCES MEETUPS(ID),
    USER_NAME VARCHAR(30) REFERENCES USERS (USERNAME),
    VOTES INTEGER NOT NULL,
    CREATED_AT TEXT  NOT NULL
    );
"""

CREATE_TABLE_RSVPS = """
    CREATE TABLE IF NOT EXISTS RSVPS (
    ID SERIAL NOT NULL,
    MEETUP INTEGER NOT NULL,
    USER_ID INTEGER NOT NULL,
    RESPONSE TEXT NOT NULL,
    PRIMARY KEY(USER_ID, MEETUP)
    );
"""

CREATE_TABLE_TOKENS = """
    CREATE TABLE IF NOT EXISTS TOKENS (
    ID SERIAL PRIMARY KEY NOT NULL,
    TOKEN VARCHAR(256)
    );
"""

CREATE_TABLE_QVOTES = """
    CREATE TABLE IF NOT EXISTS QVOTES (
    ID SERIAL NOT NULL,
    USERID INTEGER NOT NULL REFERENCES USERS (ID),
    QUESTIONID INTEGER NOT NULL REFERENCES QUESTIONS (ID),
    VOTE VARCHAR(50) NOT NULL
    );
"""

CREATE_USER = """
    INSERT INTO users (firstname, lastname, othername, email,
    phonenumber, username, isadmin, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, firstname, lastname, othername, email,
    phonenumber, username, isadmin, password;
"""

DROP_TABLES = """
    DROP TABLE IF EXISTS USERS, MEETUPS, QUESTIONS, RSVPS,
    TOKENS, QVOTES;
"""

GET_USER_BY_NAME = """
        SELECT * FROM USERS WHERE username = %s"""

GET_BY_EMAIL = """
        SELECT * FROM USERS WHERE email = %s"""

GET_USER_BY_ID = """
    SELECT id, firstname, lastname, othername, email,
    phonenumber, username, isadmin, password FROM USERS WHERE  id = %s"""

GET_ALL_USERS = """
    SELECT * FROM USERS ORDER BY id"""

CREATE_TOKEN = """
    INSERT INTO tokens (token) VALUES (%s)
    RETURNING token;
"""

GET_TOKEN = """
    SELECT token FROM tokens WHERE token = %s
"""

CREATE_MEETUP = """
    INSERT INTO meetups (topic, images, location, happening_on,
    tags) VALUES (%s, %s, %s, %s, %s) RETURNING
    id, topic, images, location, happening_on,
    tags;
"""

GET_ALL_MEETUPS = """
    SELECT * FROM meetups ORDER BY id
"""

GET_MEETUP_BY_ID = """
    SELECT * FROM meetups WHERE id = %s
"""

VERIFY_MEETUP = """
    SELECT * FROM meetups WHERE (topic, tags, location) = (%s, %s, %s)
"""

DELETE_MEETUP = """
    DELETE FROM meetups WHERE id = %s
"""

VERIFY_QUESTION = """
        SELECT * FROM questions where
        (title, body, meetup) = (%s, %s, %s)
"""

CREATE_QUESTION = """
    INSERT INTO questions (title, body, meetup, user_name, votes, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id, title, body, meetup, user_name, votes, created_at;
"""

GET_ALL_QUESTIONS = """
        SELECT * FROM questions ORDER BY id
"""

GET_QUESTION_BY_ID = """
        SELECT * FROM questions WHERE id = %s
"""
DELETE_QUESTION = """
    DELETE FROM questions where id = %s
"""

GET_QUESTION_VOTES = """
    SELECT votes FROM questions where id = %s
"""

UPDATE_QUESTION_VOTES = """
    UPDATE questions
    SET votes = %s WHERE id = %s
    RETURNING *;
"""
CREATE_QUESTION_VOTE = """
    INSERT INTO qvotes (userid, questionid, vote)
    VALUES (%s, %s, %s)
    RETURNING userid, questionid, vote;
"""

GET_VOTED_QUESTION = """
    SELECT * FROM qvotes WHERE
    (userid, questionid, vote) = (%s, %s, %s)
"""

DELETE_VOTED_QUSER = """
    DELETE FROM qvotes WHERE (id, userid, questionid, vote)
    = (%s, %s, %s, %s)
"""

VERIFY_RSVP = """
    SELECT * FROM rsvps WHERE
    (meetup, user_id, response) = (%s, %s, %s)

"""

CREATE_RSVP = """
    INSERT INTO rsvps (meetup, user_id, response)
    VALUES (%s, %s, %s) RETURNING id, meetup, user_id,
    response;
"""

GET_USER_RSVPS = """
    SELECT DISTINCT meetup, response FROM rsvps WHERE
    user_id = %s
"""
