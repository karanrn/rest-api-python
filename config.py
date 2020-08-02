import os

config = {
    "dev": "config.Development",
    "prod": "config.Production"
}

class BaseConfig(object):
    """ Base config class. This fields will use by production and development server """


class Development(BaseConfig):
    """ Development config. We use Debug mode """
    HOST = os.environ['DB_HOST']
    PORT = 3306
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']
    DEBUG = True
    TESTING = False
    ENV = 'dev'
    APPNAME = "WebAPIDev"
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = os.environ['SECRET_KEY']

class Production(BaseConfig):
    """ Production config. We use Debug mode false """

    HOST = os.environ['DB_HOST']
    PORT = 3306
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']
    DEBUG = True
    TESTING = False
    ENV = 'prod'
    APPNAME = "WebAPIProd"
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = os.environ['SECRET_KEY']

def configure_app(app):
    """ App coniguration will be here"""
    env = os.environ['ENV']
    app.config.from_object(config[env])