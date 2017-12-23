## RESTful Feature requests app

- Flask

1. Create a env file in the base directory after cloning the app. Refer to example [here](https://github.com/dhruvsingh/feature-requests/blob/master/.env_example)
2. Create a virtual environment (python 3.x) and activate it (I've used [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):
    - cd feature-requests
    - mkvirtualenv feature-requests --python=/usr/bin/python3
    - workon feature-requests
3. Install required libraries: pip install -r requirements.txt.
4. run ./manage.py createdb
5. run ./manage.py runserver to start the local dev server
6. Browse to http://localhost:5000 to access the app.


The app can also be accessed [here]().