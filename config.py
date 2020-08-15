import os

from flask import Flask

config = {
    "development": "config.Development",
    "production": "config.Production"
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
    DEBUG = False
    TESTING = False
    APPNAME = "WebAPIProd"
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = os.environ['SECRET_KEY']

def configure_app(app: Flask) -> None:
    """ App coniguration will be here"""
    env = os.environ['FLASK_ENV']
    app.config.from_object(config[env])