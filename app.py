from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from configparser import ConfigParser
import sqlalchemy as db

# Config parser
config = ConfigParser()
config.read('config.ini')

# Database connection parameters
db_user = config['database']['user']
db_pwd = config['database']['password']
db_host = config['database']['host']
db_port = config['database']['port']
db_name = config['database']['name']

connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connect to database
engine = db.create_engine(connection_str)

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Welcome!"

@app.route('/users/<int:emp_id>')
def show_user(emp_id):
    try:
        connection = engine.connect()
        
        get_user_query = """SELECT emp_id, first_name, last_name, job_title, dob
                         FROM employee where emp_id = %s;
                         """
        db_result = connection.execute(get_user_query, emp_id)

        result = []
        for res in db_result:
            record = {
                'emp_id': res['emp_id'],
                'first_name': res['first_name'],
                'last_name': res['last_name'],
                'dob': res['dob']
            }
            result.append(record)

        return jsonify({'data':result}), 200

    except Exception as ex:
        print(ex)
        return abort(500)

@app.route('/users', methods=['POST'])
def add_user():
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

        return jsonify({'user': user}), 201
    
    except Exception as ex:
        print(ex)
        return abort(500)
    
    finally:
        connection.close()

if __name__ == "__main__":
    app.run()