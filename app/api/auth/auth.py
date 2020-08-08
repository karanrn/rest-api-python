from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
from flask import redirect

from app.errors import bad_request
from app import bcrypt
from app.data.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    """ Signup new user """
    try:
        if not request.json or not 'email_id' in request.json \
            or not 'password' in request.json:
            return bad_request('Email_id and/or password is missing!')
        
        email = request.json.get('email_id')
        password = request.json.get('password')
        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token(user.id)

        responseObj = {
            'status': 'Success',
            'message': 'Successfully signed up.',
            'auth_token': auth_token.decode()
        }
        
        return jsonify(responseObj), 201, {'Content-Type': 'application/json'}
    except Exception as ex:
        print(ex)
        return 'try again', 401

@auth.route('/login', methods=['POST'])
def signin():
    """ Login user """
    try:
        if not request.json or not 'email_id' in request.json \
            or not 'password' in request.json:
            return bad_request('Email_id and/or password is missing!')

        email = request.json.get('email_id')
        password = request.json.get('password')

        user = db.session.query(User).filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                auth_token = user.encode_auth_token(user.id)
                
                responseObj = {
                'status': 'Success',
                'message': 'Successfull login.',
                'auth_token': auth_token.decode()
                }
            
                return jsonify(responseObj), 201, {'Content-Type': 'application/json'}
        else:
            return redirect("signup", code=303)
    
    except Exception as ex:
        print(ex)
        return 'try again', 401    