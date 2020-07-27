from app import app
from webapi.data.models_new import db

with app.app_context():
    db.create_all()