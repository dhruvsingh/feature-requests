import os

from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_env_var(name, default=None):
    u"""
    Get the environment variables.

    The function tries to get the variable var_name from the environment,
    and if it doesn’t find it, it raises an ImproperlyConfigured error.
    """
    try:
        return os.environ[name]
    except KeyError:
        if default:
            return default
        raise ImportError(
            'Set the {0} environment variable.'.format(name)
        )


def read_env():
    u"""
    Read the environment variables from .env file.

    Define the PATH for the .env file and Load the .env
    """
    dotenv_path = os.path.join(BASE_DIR, '.env')
    try:
        load_dotenv(dotenv_path)
    except IOError:
        raise
        pass

# load environment variables from .env file
read_env()

env = get_env_var('SETTINGS_MODULE', 'DevelopmentConf')
app.config.from_object(env)
app.config['ENV'] = env

# guess this is the standard way as to how Flask works
# some apps suggest doing this on the wsgi file
# doing it here to support dev work using the inbuilt dev server
from fr_app import views
