"""
    This module contains the database queries used in the application models
"""

CREATE_TABLE_USERS = """
    CREATE TABLE IF NOT EXISTS USERS (
    ID SERIAL PRIMARY KEY NOT NULL,
    FIRSTNAME VARCHAR(60) NOT NULL,
    LASTNAME VARCHAR(60) NOT NULL,
    OTHERNAME VARCHAR(50),
    EMAIL VARCHAR(40) NOT NULL,
    PHONENUMBER INTEGER NOT NULL,
    USERNAME VARCHAR(30) NOT NULL,
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
    HAPPENING_ON DATE NOT NULL DEFAULT CURRENT_DATE,
    TAGS TEXT []
    );
"""

CREATE_TABLE_QUESTIONS = """
    CREATE TABLE IF NOT EXISTS QUESTIONS (
    ID SERIAL PRIMARY KEY NOT NULL,
    TITLE VARCHAR(40) NOT NULL,
    BODY VARCHAR(40) NOT NULL,
    CREATED_BY INTEGER REFERENCES USERS (ID),
    MEETUP INTEGER REFERENCES MEETUPS(ID),
    VOTES INTEGER NOT NULL,
    CREATED_AT DATE DEFAULT CURRENT_DATE
    );
"""

CREATE_TABLE_RSVPS = """
    CREATE TABLE IF NOT EXISTS RSVPS (
    ID SERIAL NOT NULL,
    MEETUP INTEGER NOT NULL,
    USER_ID INTEGER NOT NULL,
    PRIMARY KEY(USER_ID, MEETUP)
    );
"""

CREATE_TABLE_TOKENS = """
    CREATE TABLE IF NOT EXISTS TOKENS (
    ID SERIAL PRIMARY KEY NOT NULL,
    TOKEN VARCHAR(256)
    );
"""

CREATE_USER = """
    INSERT INTO users (firstname, lastname, othername, email,
    phonenumber, username, isadmin, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING firstname, lastname, othername, email,
    phonenumber, username, isadmin, password;
"""

DROP_TABLES = """
    DROP TABLE IF EXISTS USERS, MEETUPS, QUESTIONS, RSVPS,
    TOKENS;
"""

GET_USER_BY_NAME = """
        SELECT firstname, lastname, othername, email,
    phonenumber, username, isadmin, password FROM USERS WHERE username = %s"""

GET_BY_EMAIL = """
        SELECT firstname, lastname, othername, email,
    phonenumber, username, isadmin, password FROM USERS WHERE email = %s"""

GET_USER_BY_ID = """
    SELECT firstname, lastname, othername, email,
    phonenumber, username, isadmin, password FROM USERS WHERE  id = %s"""

GET_ALL_USERS = """
    SELECT * FROM USERS ORDER BY id"""
