from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
# from configparser import ConfigParser
# import sqlalchemy as db

from webapi.data.models import User

user = Blueprint('user', __name__)

# #Config parser
# config = ConfigParser()
# config.read('/home/karan/WebAPI-Python/config.ini')

# # Database connection parameters
# db_user = config['database']['user']
# db_pwd = config['database']['password']
# db_host = config['database']['host']
# db_port = config['database']['port']
# db_name = config['database']['name']

# connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# # connect to database
# engine = db.create_engine(connection_str)

@user.route('/', methods=['GET'])
def get_users():
    try:
        args = request.args
        limit = 50 # Default limit
        offset = 0 # Default offset
        
        # Pagination
        if "limit" in args:
            try:
                limit = int(args["limit"])
            except ValueError:
                return "Limit value should be an integer", 400

        if "offset" in args:
            try:
                offset = int(args["offset"])
            except ValueError:
                return "Offset value should be an integer", 400

        response = User.fetch_all_users(limit, offset)
        
        return response, 200, {'Content-Type': 'application/json'}

    except Exception as ex:
        print(ex)
        return abort(500)

@user.route('/<int:emp_id>', methods=['GET'])
def get_user(emp_id):
    try:
        result = User.fetch_user(emp_id)
        return jsonify({'data':result}), 200, {'Content-Type': 'application/json'}

    except Exception as ex:
        print(ex)
        return abort(500)

@user.route('/register', methods=['POST'])
def register():
    try:
        if not request.json or not 'first_name' in request.json \
            or not 'dob' in request.json or not 'emp_id' in request.json:
            return abort(400)
        
        new_user = {
            'emp_id' : request.json.get('emp_id'),
            'first_name': request.json['first_name'],
            'last_name': request.json.get('last_name', None),
            'job_title': request.json.get('job_title', None),
            'dob': request.json.get('dob', None)
        }

        response = User.add_user(new_user)
        
        return response, 201, {'Content-Type': 'application/json'}
    
    except Exception as ex:
        print(ex)
        return abort(500)

@user.route('/update/<int:emp_id>', methods=['PUT'])
def update_user(emp_id):
    try:
        if not request.json or not 'first_name' in request.json \
            or not 'dob' in request.json:
            return abort(400)
        
        user_details = {
            'first_name': request.json['first_name'],
            'last_name': request.json.get('last_name', None),
            'job_title': request.json.get('job_title', None),
            'dob': request.json.get('dob')
        }
        
        response = User.update_user(emp_id, user_details)

        return response, 200, {'Content-Type': 'application/json'}

    except Exception as ex:
        print(ex)
        return abort(500)
