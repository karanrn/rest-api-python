from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify

#from webapi.data.models import User

user = Blueprint('user', __name__)

from configparser import ConfigParser
import sqlalchemy as db

# Config parser
config = ConfigParser()
config.read('/home/karan/WebAPI-Python/config.ini')

# Database connection parameters
db_user = config['database']['user']
db_pwd = config['database']['password']
db_host = config['database']['host']
db_port = config['database']['port']
db_name = config['database']['name']

connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connect to database
engine = db.create_engine(connection_str)

# @user.route('/', methods=['GET'])
# def hello_world():
#     return "Welcome!"

@user.route('/', methods=['GET'])
def get_users():
    try:
        connection = engine.connect()
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


        # Default query 
        get_all_users = """ SELECT id, first_name, last_name, job_title, dob
                         FROM employee LIMIT {limit} OFFSET {offset};
                         """.format(limit=limit, offset=offset)

        db_result = connection.execute(get_all_users)

        result = []
        for res in db_result:
            record = {
                'emp_id': res['id'],
                'first_name': res['first_name'],
                'last_name': res['last_name'],
                'job_title': res['job_title'],
                'dob': res['dob']
            }
            result.append(record)
        
        if len(result) == 0:
            links = {}
        else:
            links = {
                "next": "http://localhost:5000/users?limit={limit}&offset={offset}"
                .format(limit=limit, offset=offset+limit)
            }
        
        response = {
            "pagination": {
                "offset": offset,
                "limit": limit 
            },
            "data": result,
            "links": links
        }
        return response, 200

    except Exception as ex:
        print(ex)
        return abort(500)
    
    finally:
        connection.close()

@user.route('/<int:emp_id>', methods=['GET'])
def get_user(emp_id):
    try:
        connection = engine.connect()
        
        get_user_query = """SELECT id, first_name, last_name, job_title, dob
                         FROM employee where id = %s;
                         """
        db_result = connection.execute(get_user_query, emp_id)

        result = []
        for res in db_result:
            record = {
                'emp_id': res['id'],
                'first_name': res['first_name'],
                'last_name': res['last_name'],
                'job_title': res['job_title'],
                'dob': res['dob']
            }
            result.append(record)

        return jsonify({'data':result}), 200

    except Exception as ex:
        print(ex)
        return abort(500)
    
    finally:
        connection.close()

@user.route('/register', methods=['POST'])
def register():
    try:
        connection = engine.connect()

        if not request.json or not 'first_name' in request.json \
            or not 'dob' in request.json:
            return abort(400)
        
        user = {
            'first_name': request.json['first_name'],
            'last_name': request.json.get('last_name', None),
            'job_title': request.json.get('job_title', None),
            'dob': request.json.get('dob', None)
        }

        insert_query = """INSERT INTO employee (first_name, last_name, job_title, dob)
                            VALUES
                            (%s, %s, %s, %s);
                        """

        connection.execute(insert_query, (user['first_name'],
                                        user['last_name'],
                                        user['job_title'],
                                        user['dob']))

        return "New employee enrolled", 201
    
    except Exception as ex:
        print(ex)
        return abort(500)
    
    finally:
        connection.close()

@user.route('/update/<int:emp_id>', methods=['PUT'])
def update_user(emp_id):
    try:
        connection = engine.connect()

        if not request.json or not 'first_name' in request.json \
            or not 'dob' in request.json:
            return abort(400)
        
        user = {
            'first_name': request.json['first_name'],
            'last_name': request.json.get('last_name', None),
            'job_title': request.json.get('job_title', None),
            'dob': request.json.get('dob', None)
        }
        
        update_user_query = """UPDATE employee 
                        set first_name = %s, 
                        last_name = %s, 
                        job_title = %s, 
                        dob = %s
                        where id = %s;
                         """
        connection.execute(update_user_query, (user['first_name'],
                                        user['last_name'],
                                        user['job_title'],
                                        user['dob'],
                                        emp_id))

        return "Employee {} information is updated".format(emp_id), 200

    except Exception as ex:
        print(ex)
        return abort(500)
    
    finally:
        connection.close()
