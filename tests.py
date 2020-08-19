import os
import unittest
from flask import current_app as app

from app import create_app
from app.data.models import db
from app.data.models import User
from app.data.models import Employee

class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

    def setUp(self):
        with self.app.app_context():
            self.client =  app.test_client()
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_Get_Employees(self):
        with self.app.app_context():
            # Correct endpoint
            good_response = self.client.get('/api/employees')
            self.assertEqual(good_response.status_code, 200)

            # Wrong endpoint
            bad_response = self.client.get('/employees')
            self.assertEqual(bad_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
