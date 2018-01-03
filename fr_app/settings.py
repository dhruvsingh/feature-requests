from fr_app import get_env_var


class BaseConf(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_env_var(
        'DATABASE_URL',
        default="sqlite:///:memory:"
    )
    SECRET_KEY = get_env_var('SECRET_KEY', default='some_secret_key')


class ProductionConf(BaseConf):
    DEBUG = False


class DevelopmentConf(BaseConf):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConf(DevelopmentConf):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
