from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
import json

from webapi.data.models import Employee
from webapi import db

employee = Blueprint('employees', __name__)

@employee.route('/', methods=['GET'])
def get_employees():
    try:
        args = request.args
        per_page = 20
        page = 1
        # Pagination
        if "page" in args:
            try:
                page = int(args["page"])
            except ValueError:
                return "Page value should be an integer", 400

        employees = db.session.query(Employee).order_by(Employee.emp_id).paginate(page, per_page, error_out=False)
        
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

@employee.route('/register', methods=['POST'])
def register():
    try:
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
        db.session.flush()
        db.session.commit()
        
        return jsonify({'employee': employee.serialize}), 201, {'Content-Type': 'application/json'}
    
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return abort(500)

@employee.route('/update/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    try:
        employee = db.session.query(Employee).filter_by(emp_id=emp_id).first_or_404()

        print(request.json['first_name'], request.json['dob'])
        if not request.json or not 'first_name' in request.json \
            or not 'dob' in request.json:
            return bad_request('First_name or/and dob field(s) is/are missing')
        
        employee.first_name = request.json['first_name'],
        employee.last_name = request.json.get('last_name', None),
        employee.job_title = request.json.get('job_title'),
        employee.dob = request.json.get('dob')

        db.session.flush()
        db.session.commit()
        
        return jsonify(f'Employee {emp_id} details updated'), 200, {'Content-Type': 'application/json'}

    except Exception as ex:
        db.session.rollback()
        print(ex)
        return abort(500)

# Custom Error Helper Functions
def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response
