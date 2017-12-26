from fr_app import get_env_var


class BaseConf(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_env_var('DATABASE_URL')
    RECAPTCHA_PUBLIC_KEY = get_env_var('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = get_env_var('RECAPTCHA_PRIVATE_KEY')
    SECRET_KEY = get_env_var('SECRET_KEY', default='some_secret_key')


class ProductionConf(BaseConf):
    DEBUG = False


class DevelopmentConf(BaseConf):
    DEBUG = True
    SQLALCHEMY_ECHO = True
