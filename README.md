# REST API implementation in Python
An attempt to understand implmentation of a good REST API using Python. <br>
I have used flask microframework to implement the REST API.

## Good practices of REST API
1. Use Nouns in URI
2. Let HTTP Verb define Action
3. Pagination
4. Searching/Filtering
5. API Versioning

API performs CRUD operations on employees, authentication is implemented using JWT.


## Setup and launch API
1. Run MySQL database on port 3306.
2. Export environment variables for the API
```
# Flask entry point
export FLASK_APP=app.py

# Database details
export DB_HOST=localhost
export DB_USER=app_user
export DB_PASSWORD=app@123
export DB_NAME=test

# Environment type
export ENV=dev

# Secret key for JWT encoding
export SECRET_KEY=abc#123@789
``` 
3. Run Setup to create tables basis models
```
python setup.py
```
4. Launch the API
```
flask run
```

## REST API operations
### Authentication:
1. Signup - 
```
curl -X POST -H "Content-Type: application/json" -d "@user.json" http://localhost:5000/api/auth/signup
```
2. Login - 
```
curl -X POST -H "Content-Type: application/json" -d "@user.json" http://localhost:5000/api/auth/login
```

A sample user request for authentication - 
```
{
    "email_id": "User007@gmail.com",
    "password": "Pass@123"
}
```

### GET operation:
1. Get all employees and traverse with pages -
```
curl -X GET http://localhost:5000/api/employees
curl -X GET http://localhost:5000/api/employees?page=2
```
2. Get employees filtered on employee's first_name - 
```
curl -X GET http://localhost:5000/api/employees?first_name=John
```
3. Get employee based on employee Id (emp_id) - 
```
curl -X GET http://localhost:5000/api/employees/101
```

### POST operation:
Addition of new employee can only be performed by authenticated user by passing JWT token received from login/signup.
```
curl -X POST -H "Content-Type: application/json" -H "x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTY4NTU2MjUsImlhdCI6MTU5Njg1NTUwNSwic3ViIjozfQ.OiaQtzeGD8vj3LLxqTkaUrYj2VhKTsJSqKtumm9cpZs" -d "@emp.json" http://localhost:5000/api/employees
```

### PUT operation:
Updating of employee details can only be performed by authenticated user by passing JWT token received from login/signup.
```
curl -X PUT -H "Content-Type: application/json" -H "x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTY4NTU2MjUsImlhdCI6MTU5Njg1NTUwNSwic3ViIjozfQ.OiaQtzeGD8vj3LLxqTkaUrYj2VhKTsJSqKtumm9cpZs" -d "@emp.json" http://localhost:5000/api/employees/101
```

### DELETE operation:
Deletion of an employee can only be performed by authenticated user by passing JWT token received from login/signup.
```
curl -X POST -H "Content-Type: application/json" -H "x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTY4NTU2MjUsImlhdCI6MTU5Njg1NTUwNSwic3ViIjozfQ.OiaQtzeGD8vj3LLxqTkaUrYj2VhKTsJSqKtumm9cpZs" http://localhost:5000/api/employees/101
```

---
## Read more - 
1. [Good practices of REST API](https://medium.com/hashmapinc/rest-good-practices-for-api-design-881439796dc9)
2. [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/)
3. [JSON Web Token](https://jwt.io/introduction/)
4. [REST API versioning](https://restfulapi.net/versioning/)
