import sqlalchemy as db
from typing import List
from typing import Dict
from webapi import app

# Database connection parameters
db_user = app.config['DB_USER']
db_pwd = app.config['DB_PASSWORD']
db_host = app.config['HOST']
db_port = app.config['PORT']
db_name = app.config['DB_NAME']

connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connect to database
engine = db.create_engine(connection_str)

class User:
    """ Data access layer for user/employee """
    def fetch_all_users(limit:int, offset:int) -> List[Dict[str, str]]:
        try:
            connection = engine.connect()

            # Default query 
            get_all_users = """ SELECT emp_id, first_name, last_name, job_title, dob
                            FROM employee ORDER BY emp_id LIMIT {limit} OFFSET {offset};
                            """.format(limit=limit, offset=offset)

            db_result = connection.execute(get_all_users)

            result = []
            for res in db_result:
                record = {
                    'emp_id': res['emp_id'],
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

            return response
        
        except Exception as ex:
            raise ex
        
        finally:
            connection.close()

    def fetch_user(emp_id:int) -> List[Dict[str, str]]:
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
                    'job_title': res['job_title'],
                    'dob': res['dob']
                }
                result.append(record)

            if len(result) == 0:
                result = "No employee with employee ID: {}".format(emp_id)

            return result

        except Exception as ex:
            raise ex
        
        finally:
            connection.close()

    def add_user(user:Dict[str, str]) -> str:
        try:
            connection = engine.connect()

            insert_query = """INSERT INTO employee (emp_id, first_name, last_name, job_title, dob)
                                VALUES
                                (%s, %s, %s, %s, %s);
                            """

            connection.execute(insert_query, (user['emp_id'],
                                            user['first_name'],
                                            user['last_name'],
                                            user['job_title'],
                                            user['dob']))

            return "Employee with Id {} is enrolled."
        
        except Exception as ex:
            raise ex
        
        finally:
            connection.close()

    def update_user(emp_id:int, user_details:Dict[str, str]) -> str:
        try:
            connection = engine.connect()
            
            update_user_query = """UPDATE employee 
                            set first_name = %s, 
                            last_name = %s, 
                            job_title = %s, 
                            dob = %s
                            where emp_id = %s;
                            """
            connection.execute(update_user_query, (user_details['first_name'],
                                            user_details['last_name'],
                                            user_details['job_title'],
                                            user_details['dob'],
                                            emp_id))

            return "Employee {} information is updated".format(emp_id)

        except Exception as ex:
            raise ex
        
        finally:
            connection.close()
