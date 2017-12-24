from fr_app import get_env_var


class BaseConf(object):
    SECRET_KEY = get_env_var('SECRET_KEY', default='some_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = get_env_var('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = get_env_var('RECAPTCHA_PRIVATE_KEY')


class ProductionConf(BaseConf):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/feature-requests'


class DevelopmentConf(BaseConf):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
