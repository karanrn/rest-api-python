import datetime
from typing import Dict
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import jwt

from app import bcrypt

db = SQLAlchemy()

class Employee(db.Model):
    """ Data access layer for employee """
    __tablename__ = 'employee'

    emp_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20))
    job_title = db.Column(db.String(100), nullable = False)
    dob = db.Column(db.DateTime, nullable = False)

    def __init__(self, emp_id, first_name, last_name, job_title, dob):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.dob = dob
    
    @property
    def serialize(self) -> Dict[str, Any]:
        """Return object data in easily serializable format"""
        return {
            'emp_id': self.emp_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'job_title': self.job_title,
            'dob': self.dob
        }

class User(db.Model):
    """User model for stroing user details"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id:int) -> bytes:
        """ Generates auth token """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=2),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )

        except Exception as ex:
            print(ex)
            return ex
    
    @staticmethod
    def decode_auth_token(auth_token: str) -> str:
        """ Validates auth token """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'