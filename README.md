
[![Build Status](https://travis-ci.org/hogum/qstioner-v2.svg?branch=develop)](https://travis-ci.org/hogum/qstioner-v2) [![Coverage Status](https://coveralls.io/repos/github/hogum/qstioner-v2/badge.svg?branch=ch-ci-badges-163341965)](https://coveralls.io/github/hogum/qstioner-v2?branch=ch-ci-badges-163341965)
[![Maintainability](https://api.codeclimate.com/v1/badges/0cbd787bf7490e88c6f8/maintainability)](https://codeclimate.com/github/hogum/qstioner-v2/maintainability)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/4e960f4340da75ae0cff)
# qstioner-v2
Questioner api is an api version 2 of the qstioner web application. It allows the user to send htttp requests to application and persists the application records in a postgres database.
Questioner is a platform where human beings can ask questions about meetups and vote present questions.


## API
### Installation
- Create a new directory locally and open a terminal window from that folder
- Clone the repository
```shell
$ git clone https://github.com/hogum/qstioner-v2.git
```
- Switch to the qstioner-v2 directory
```shell
$ cd qstioner-v2
```
- Depending on your os install virtualenv and open a virtual enviroment:
``` shell
$ pip install virtualenv
```
``` shell
$ virtualenv venv && source venv/bin/activate
```
- Install the project requirements
```shell
$ pip install -r requirements.txt
```
- Set Up the environment variables


### Running the application
Edit the env_sample file to have your preferred environment settings
The following will be required: 

``` shell
$ DATABASE
$ DATABASE_HOST
$ DATABSE_USER
$ DATABASE_PASSW
```
If using windows, simply replace occurrences of `export` in the env_sample with `set`
Source the file

```shell 
$ source .env_sample
```

##### Start the server
``` shell
$ flask run
```

### Project Dependencies
- [Flask](http://flask.pocoo.org/): For creation of the Web Framework
- [Python 3](https://www.python.org/): The programming Language
- [Flask-RESTful](https://flask-restful.readthedocs.io/): Development of the API
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/): Authentication of Protected endpoints
- [Psycopg2 Binary](http://initd.org/psycopg/): Postgres database adaption
- [Flassger](https://github.com/rochacbruno/flasgger): Swagger Documentation
- [Pytest](https://pytest.org/): Application testing
- [Travis CI](https://travis-ci.org/): Continuous Integration and Builds
- [Coveralls](https://coveralls.io/): Test Coverage History


### Endpoints

##### Authorization Endpoints
- Allows Registration and Login of users into the application

Method | Endpoint | Functionality
--- | --- |---
POST | `api/v1/auth/register` | Register new User
POST | `api/v1/auth/login` | Login registered User
PUT | `api/v1/auth/users/user_id` | Update user details
DELETE | `api/v1/auth/logout` | Logout a logged in user
DELETE | `api/v1/auth/users/user_id` | Delete a user account


##### Meetup Endpoints

- Allows management of meetups by the admin, and all CRUD operations on a meetup

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/meetups/` | Add a meetup
GET | `/api/v1/meetups/upcoming` | Lists all meetups 
GET | `/api/v1/meetups/<meetup_id>` | Retrieve a meetup 
PUT | `/api/v1/meetups/<meetup_id>` | Edit a meetup of a logged in user
POST | `/api/v1/meetup/<meetup_id>/<tag>` | Post a tag to a meetup
GET | `/api/v1/meetup/<tag>` | Get all meetups that match a tag
DELETE | `/api/v1/meetups/<question_id>` | Delete a meetup of a logged in admin user


##### Questions Endpoints
- Allows users to perform CRUD operations on questions to a meetup

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/questions` | Add a question
GET | `/api/v1/questions` | Lists all questions 
GET | `/api/v1/meetups/<meetup_id>/questions/<question_id>` | Retrieve a question 
PUT | `/api/v1/questions/<question_id>` | Edit a question of a logged in user
DELETE | `/api/v1/questions/<question_id>` | Delete a question of a logged in user


##### Vote Endpoints

Method | Endpoint | Functionality
--- | --- | ---
PATCH | `/api/v1/<question_id>/upvote` | Upvote a Question
PATCH | `/api/v1/<question_id>/downvote` | Downvote a Question


##### RSVP Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/<meetup_id>/<rsvp>` | RSVP a meetup
GET | `api/v1/meetups/{user_id/username}/rsvp` | Fetch Meetups RSVP-ed by user


##### Comment Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/questions/<question_id>/comment` | Add a Comment to a Meetup Question
GET | `/api/v1/questions/<question_id>/comment` | Lists all comments to a Question
GET | `/api/v1/questions/<question_id>/{username/user_id}/comment` | Get a User's comments to a Question
PUT | `/api/v1/comments/commentID` | Edit a comment
DELETE | `/api/v1/comments/commentID` | Delete a comment


##### Contributors

[Mugoh](https://github.com/hogum)

##### Acknowledgment
This software was developed with the support of [Andela](https://github.com/andela) Kenya
