from fr_app import get_env_var


class BaseConf(object):
    SECRET_KEY = get_env_var('SECRET_KEY', default='some_secret_key')


class ProductionConf(BaseConf):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/feature-requests'


class DevelopmentConf(BaseConf):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://features.db'
    SQLALCHEMY_ECHO = True
