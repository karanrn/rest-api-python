from flask import Flask

def create_app():
    # Flask app initialization
    app = Flask(__name__)

    from config import configure_app

    # Configure app
    configure_app(app)

    app.url_map.strict_slashes = False
    
    from webapi.api.user.controllers import user
    app.register_blueprint(user, url_prefix='/api/users')

    return app