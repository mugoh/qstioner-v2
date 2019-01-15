
[![Build Status](https://travis-ci.org/hogum/qstioner-api.png?branch=develop)](https://travis-ci.org/hogum/qstioner-api) [![Coverage Status](https://coveralls.io/repos/github/hogum/qstioner-api/badge.svg?branch=ch-ci-badges-163075084)](https://coveralls.io/github/hogum/qstioner-api?branch=ch-ci-badges-163075084)
[![Maintainability](https://api.codeclimate.com/v1/badges/0a723df98c0d910d94bb/maintainability)](https://codeclimate.com/github/hogum/qstioner-api/maintainability)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/4e960f4340da75ae0cff)
# qstioner-api
Questioner api is an api version 1 of the qstioner web application. It allows the user to send htttp requests to application and persists in data structures.
Questioner is a platform where human beings can ask questions about meetups and vote present questions.


## API
### Installation
- Create a new directory locally and open a terminal window from that folder
- Clone the repository
```shell
$ git clone https://github.com/hogum/qstioner-api.git
```
- Switch to the stackS directory
```shell
$ cd qstioner-api
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
``` shell
$ export JWT_SECRET_KEY="your jwt secret key"
$ export SECRET_KEY="your secret key"
```

```shell 
$ export FLASK_APP=app
```
or
```shell
$ set FLASK_APP=app
```
on Windows OS
##### Start the server
``` shell
$ flask run
```

### Project Dependencies
- [Flask](http://flask.pocoo.org/): For creation of the Web Framework
- [Python 3](https://www.python.org/): The programming Language
- [Flask-RESTful](https://flask-restful.readthedocs.io/): Development of the API
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
DELETE | `api/v1/auth/users/user_id` | Delete a user account


##### Meetup Endpoints

- Allows management of meetups by the admin, and all CRUD operations on a meetup

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/meetups/` | Add a meetup
GET | `/api/v1/meetups/upcoming` | Lists all meetups 
GET | `/api/v1/meetups/meetup_id` | Retrieve a meetup 
PUT | `/api/v1/meetups/meetup_id` | Edit a meetup of a logged in user
DELETE | `/api/v1/meetups/question_id` | Delete a request of a logged in user

##### Questions Endpoints
- Allows users to perform CRUD operations on questions to a meetup

Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/meetups/meetup_id/questions` | Add a question
GET | `/api/v1/meetups/meetup_id/questions` | Lists all questions 
GET | `/api/v1/meetups/meetup_id/questions/question_id` | Retrieve a question 
PUT | `/api/v1/meetups/meetup_id/questions/question_id` | Edit a question of a logged in user
DELETE | `/api/v1/meetups/meetup_id/questions/question_id` | Delete a request of a logged in user


##### Vote Endpoints

Method | Endpoint | Functionality
--- | --- | ---
PATCH | `/api/v1/question_id/upvote` | Upvote a Question
PATCH | `/api/v1/question_id/downvote` | Downvote a Question

##### RSVP Endpoints

Method | Endpoint | Functionality
--- | --- | ---
PATCH | `/api/v1/meetup_id/<rsvp>` | RSVP a meetup


##### Comment Endpoints


Method | Endpoint | Functionality
--- | --- | ---
POST | `/api/v1/meetups/meetup_id/questions/question_id/comment` | Add a Comment to a Meetup Question
GET | `/api/v1/meetups/meetup_id/questions/question_id/comment` | Lists all comments to a Question 
PUT | `/api/v1/meetups/meetup_id/questions/question_id/comment/commentID` | Edit a comment 
DELETE | `/api/v1/meetups/meetup_id/questions/question_id/comment/commentID` | Delete a comment


##### Contributors

[Mugoh](https://github.com/hogum)

##### Acknowledgment
This software was developed with the support of [Andela](https://github.com/andela) Kenya
