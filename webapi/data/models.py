from flask_sqlalchemy import SQLAlchemy
from typing import List
from typing import Dict

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
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'emp_id': self.emp_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'job_title': self.job_title,
            'dob': self.dob
        }
