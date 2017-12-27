#!/usr/bin/env python
import os
import json
import argparse

from fr_app import app, models

from flask_fixtures import load_fixtures


help_string = """

use as - python manage.py [command]

[command] can be replaced by one of the following:

runserver - runs the flask local server

create_db - create the initial database tables

init_db - populate the database with initial data. Make sure to run this
after create_db is run.

drop_db - drop the current database with data

"""


description = """Utility function for running various flask commands."""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('command', help=help_string)
    args = parser.parse_args()

    if args.command == 'runserver':
        app.run()
    elif args.command == 'drop_db':
        models.db.drop_all()
    elif args.command == 'create_db':
        models.db.create_all()
    elif args.command == 'init_db':
        # initialize data for the created db
        fixture_dir_path = os.path.join('fr_app', 'fixtures')
        # we know that no dirs are there in the fixtures path, so safe to
        # iterate
        for fixture in os.listdir(fixture_dir_path):
            fixture_path = os.path.join(fixture_dir_path, fixture)
            with open(fixture_path, 'r') as infile:
                load_fixtures(models.db, json.loads(infile.read()))
