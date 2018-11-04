# retwitter
Postman Service Internship Assignment
![Python](https://img.shields.io/badge/Python-3.6-green.svg)
![Django](https://img.shields.io/badge/Django-2.1-orange.svg)

[![Build Status](https://travis-ci.org/sid22/retwitter.svg?branch=master)](https://travis-ci.org/sid22/retwitter)

Re Twitter Assignment - complete with all basic, extended and extra credit functionalities.

## Table of contents
- [Installation](#installation)
    - [Setup instructions](#setup-instructions)

- [Basic functionality](#basic-functionality):
    - [User registration using unique username and a password](#signup)
    - [User login, with session maintainance](#login)

- [Extended Functionality](#extended-functionality):
    - Follow, unfollow
    - Create, read, delete tweet
    - Unit/Integration tests for all endpoints

- Extra Credit
    - Like/unlike a tweet
    - Retweet
    - Replies and threading

The project is a set of APIs made with the Django Framework in Python language. MongoDB database is used for storing information, MLab is used to provide Database-as-a-Service on hostel project. Redis in-memory data structure store is used as a cache store for session management, RedisLabs is used to provide it on hostel project. 

----
## Installation
[(Back to top)](#table-of-contents)

To run the project locally, firstly the user must either:
- Set a local environment variable "ENVIRONMENT" to "production" so that the local instance connects to MLab and RedisLabs
- Or have a local instance of Mongod Server ( Port: 27017 ) and Redis Server ( 6379 ) running on standard ports.

### Setup instructions
- Clone the repo https://github.com/sid22/retwitter.git

- Command: ```cd/retwitter```

- Make a virtual environment ```python3 -m venv env``` and activate it ```source env/bin/activate```

- Install the dependencies ```pip install -r requirements.txt```

- Run it  ```python manage.py runserver```

- (Optional ) To run tests ```python manage.py test --verbosity 3```

## Basic functionality
[(Back to top)](#table-of-contents)

### Signup
User registeration with unique username and password.

Route: ```http://127.0.0.1:8000/user/signup```

Method: POST


<!-- [![codecov](https://codecov.io/gh/sid22/retwitter/branch/master/graph/badge.svg)](https://codecov.io/gh/sid22/retwitter) -->