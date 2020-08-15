from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app() -> Flask:
    # Flask app initialization
    app = Flask(__name__)

    from config import configure_app

    # Configure app
    configure_app(app)

    app.url_map.strict_slashes = False

    from app.api.auth.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')

    from app.api.employee.controllers import employee
    app.register_blueprint(employee, url_prefix='/api/employees')
    
    db.init_app(app)
    bcrypt.init_app(app)

    return app