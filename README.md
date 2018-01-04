[![Build Status](https://travis-ci.org/dhruvsingh/feature-requests.svg?branch=master)](https://travis-ci.org/dhruvsingh/feature-requests)

## RESTful Feature Requests app using
- [Flask](https://readthedocs.org/projects/flask/)
- [Flask Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [Knockoutjs](http://knockoutjs.com/)
- [bootstrap v3](https://getbootstrap.com/docs/3.3/getting-started/)

Basic RESTful implementation without authenticated backend, for creating and editing feature requests.
Done to try my hands on flask, sqlalchemy and knockoutjs.

The frontend using knockoutjs calls the REST backend done with [Flask](https://readthedocs.org/projects/flask/) with the help of [Flask Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/).

The app is hosted on heroku with a postgres backend.


Running on local?, try the following steps:

1. Clone the repo using ssh/https.
2. Create a env file in the base directory. Refer to example [here](https://github.com/dhruvsingh/feature-requests/blob/master/.env_example)
3. Create a virtual environment (python 3.x) and activate it (I've used [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):
    - cd feature-requests
    - mkvirtualenv feature-requests --python=/usr/bin/python3
    - workon feature-requests
4. Install required libraries: pip install -r requirements.txt.
5. run ./manage.py create_db
6. run ./manage.py init_db, to load initial values for product areas, clients and users.
7. run ./manage.py runserver to start the local dev server
8. Browse to http://localhost:5000 to access the app.
9. Want to drop the database, use ./manage.py drop_db. (will need tp repeat step 5 and 6 for the app to run again)

Tests:
- In order to run tests, cd to the cloned repo directory, activate virtualenv and run ```python tests.py```

Note: The app uses a temporary sqllite database when running locally. Exiting the terminal will mean loss in data.

The app can also be accessed [here](https://iws-feature-requests.herokuapp.com/).
