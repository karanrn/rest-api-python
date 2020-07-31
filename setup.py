from app import app
from webapi.data.models import db

with app.app_context():
    db.create_all()