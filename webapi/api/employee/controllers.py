from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
import jwt
from functools import wraps

from webapi.errors import not_found
from webapi.errors import bad_request
from webapi.data.models import Employee
from webapi.data.models import User
from webapi import db

employee = Blueprint('employees', __name__)

@employee.route('/', methods=['GET'])
def get_employees():
    try:
        args = request.args
        per_page = 20
        page = 1

        # allowed search fields
        search_fields = ['first_name', 'last_name', 'job_title', 'dob']
        # Pagination
        if "page" in args:
            try:
                page = int(args["page"])
            except ValueError:
                return "Page value should be an integer", 400

        search_cols = [item for item in search_fields if item in args]
        
        if not bool(search_cols):
            employees = db.session.query(Employee).order_by(Employee.emp_id).paginate(page, per_page, error_out=False)
        else:
            employees = db.session.query(Employee)
            for col in search_cols:
                column = getattr(Employee, col, None)
                filt = getattr(column, 'like')(args[col])
                employees = employees.filter(filt)
            employees = employees.order_by(Employee.emp_id).paginate(page, per_page, error_out=False)
        
        result = []
        for emp in employees.items:
            result.append({
                'emp_id': emp.emp_id,
                'first_name': emp.first_name,
                'last_name': emp.last_name,
                'job_title': emp.job_title,
                'dob': emp.dob
            })
        
        links = {}
        if employees.has_prev:
            links['prev_page'] = f'http://localhost:5000/api/employees?page={employees.prev_num}'
        if employees.has_next:
            links['next_page'] = f'http://localhost:5000/api/employees?page={employees.next_num}'
        
        response = {
            'data': result,
            'links': links
        }
        return jsonify(response), 200, {'Content-Type': 'application/json'}

    except Exception as ex:
        print(ex)
        return abort(500)

@employee.route('/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    try:
        emp = db.session.query(Employee).filter_by(emp_id=emp_id).first_or_404()
        return jsonify({'data': emp.serialize}), 200, {'Content-Type': 'application/json'}

    except Exception as ex:
        print(ex)
        return not_found('Employee does not exist')

@employee.route('/', methods=['POST'])
def register():
    try:
        check_token = validate_token(request.headers)
        if check_token == 'Valid':    
            if not request.json or not 'first_name' in request.json \
                or not 'dob' in request.json or not 'emp_id' in request.json:
                return bad_request('First_name, dob or/and emp_id field(s) is/are missing')
        
            emp_id = request.json.get('emp_id'),
            first_name = request.json['first_name'],
            last_name = request.json.get('last_name', None),
            job_title = request.json.get('job_title', None),
            dob = request.json.get('dob', None)

            employee = Employee(emp_id, first_name, last_name, job_title, dob)
            
            db.session.add(employee)
            db.session.commit()
            
            return jsonify({'employee': employee.serialize}), 201, {'Content-Type': 'application/json'}

        else:
            return jsonify({'message': check_token}), 401, {'Content-Type': 'application/json'}
    
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return abort(500)

@employee.route('/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    try:
        check_token = validate_token(request.headers)
        if check_token == 'Valid':
            employee = db.session.query(Employee).filter_by(emp_id=emp_id).first_or_404()

            if not request.json or not 'first_name' in request.json \
                or not 'dob' in request.json:
                return bad_request('First_name or/and dob field(s) is/are missing')
            
            employee.first_name = request.json['first_name'],
            employee.last_name = request.json.get('last_name', None),
            employee.job_title = request.json.get('job_title'),
            employee.dob = request.json.get('dob')

            db.session.commit()
            
            return jsonify(f'Employee {emp_id} details updated'), 200, {'Content-Type': 'application/json'}

        else:
            return jsonify({'message': check_token}), 401, {'Content-Type': 'application/json'}

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return abort(500)

@employee.route('/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    try:
        check_token = validate_token(request.headers)
        if check_token == 'Valid':
            employee = db.session.query(Employee).filter_by(emp_id=emp_id).first_or_404()

            db.session.delete(employee)
            db.session.commit()

            return jsonify(f'Employee {emp_id} is deleted'), 200, {'Content-Type': 'application/json'}

        else:
            return jsonify({'message': check_token}), 401, {'Content-Type': 'application/json'}

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return bad_request(f'Employee {emp_id} does not exist')


def validate_token(headers):
    """ Validate auth token """
    token = None

    if 'x-access-token' in headers:
        token = headers['x-access-token']

    if not token:
        return 'A valid token is missing'

    try:
        data = User.decode_auth_token(token)
        if isinstance(data, int):
            return 'Valid'
        else:
            return data
    except:
        return 'Token is invalid'