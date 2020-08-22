import os
import unittest
from flask import current_app as app
import json

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
    
    def test_Add_Update_Employee(self):
        with self.app.app_context():
            new_emp = {}
            new_emp['emp_id'] = 101
            new_emp['first_name'] = 'John'
            new_emp['last_name'] = 'Wick'
            new_emp['job_title'] = 'Engineer'
            new_emp['dob'] = '1990-12-12'
            emp_json = json.dumps(new_emp)

            # Without authentication
            response = self.client.post('/api/employees', 
                data=emp_json,
                content_type='application/json')
            self.assertEqual(response.status_code, 401)
            
            # With authentication
            user = {'email_id': 'User007@gmail.com',
                'password': 'Pass@123'}
            auth_resp = self.client.post('/api/auth/signup',
                data=json.dumps(user),
                content_type='application/json')
            auth_token = json.loads(auth_resp.data.decode('utf-8'))['auth_token']
        
            response = self.client.post('/api/employees', 
                data=emp_json,
                content_type='application/json',
                headers={'x-access-token':auth_token})
            self.assertEqual(response.status_code, 201)

            # Update employee data
            mod_emp = {}
            mod_emp['first_name'] = 'John'
            mod_emp['last_name'] = 'Wick'
            mod_emp['job_title'] = 'Security Officer' # Updated job title
            mod_emp['dob'] = '1990-12-12'
            emp_json = json.dumps(mod_emp)

            response = self.client.put('/api/employees/101', 
                data=emp_json,
                content_type='application/json',
                headers={'x-access-token':auth_token})
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/api/employees/101')
            job_title = json.loads(response.data.decode('utf-8'))['data']['job_title']
            self.assertEqual(job_title, mod_emp['job_title'])
            
    

if __name__ == '__main__':
    unittest.main()
