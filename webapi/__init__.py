from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Flask app initialization
    app = Flask(__name__)

    from config import configure_app

    # Configure app
    configure_app(app)

    app.url_map.strict_slashes = False

    from webapi.api.user.controllers import employee
    app.register_blueprint(employee, url_prefix='/api/employees')
    
    db.init_app(app)

    return app