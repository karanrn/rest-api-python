import sqlalchemy as db
from typing import List
from typing import Dict
from flask import current_app as app

# # Database connection parameters
# db_user = app.config['DB_USER']
# db_pwd = app.config['DB_PASSWORD']
# db_host = app.config['HOST']
# db_port = app.config['PORT']
# db_name = app.config['DB_NAME']

# connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# # connect to database
# engine = db.create_engine(connection_str)

class User:
    """ Data access layer for user/employee """
    def get_users(limit:int, offset:int) -> List[Dict[str, str]]:
        # try:
        #     connection = engine.connect()

        #     # Default query 
        #     get_all_users = """ SELECT emp_id, first_name, last_name, job_title, dob
        #                     FROM employee ORDER BY emp_id LIMIT {limit} OFFSET {offset};
        #                     """.format(limit=limit, offset=offset)

        #     db_result = connection.execute(get_all_users)

        #     result = []
        #     for res in db_result:
        #         record = {
        #             'emp_id': res['emp_id'],
        #             'first_name': res['first_name'],
        #             'last_name': res['last_name'],
        #             'job_title': res['job_title'],
        #             'dob': res['dob']
        #         }
        #         result.append(record)
            
        #     if len(result) == 0:
        #         links = {}
        #     else:
        #         links = {
        #             "next": "http://localhost:5000/users?limit={limit}&offset={offset}"
        #             .format(limit=limit, offset=offset+limit)
        #         }
            
        #     response = {
        #         "pagination": {
        #             "offset": offset,
        #             "limit": limit 
        #         },
        #         "data": result,
        #         "links": links
        #     }

        #     return response
        
        # except Exception as ex:
        #     raise ex
        
        # finally:
        #     connection.close()
        response = []
        return response