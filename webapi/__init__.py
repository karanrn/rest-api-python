import os
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from configparser import ConfigParser

APP_ROOT = os.path.join(os.path.dirname(__file__))

def create_app(environment):
    # Flask app initialization
    app = Flask(__name__)

    from webapi.api.user.controllers import user

    app.register_blueprint(user, url_prefix='/api/users')

    return app