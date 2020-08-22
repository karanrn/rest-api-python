from functools import wraps
from typing import Union
from typing import Any
from typing import Tuple
from typing import Dict

from flask import Blueprint
from flask import request
from flask import abort
from flask import jsonify
from flask import redirect
from flask import make_response
from flask import Response

from app.errors import bad_request
from app import bcrypt
from app.data.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup() -> Union[Tuple[Response, int, Dict[str,str]], Tuple[str, int]]:
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
            'auth_token': auth_token.decode('utf-8')
        }
        
        return jsonify(responseObj), 201, {'Content-Type': 'application/json'}
    except Exception as ex:
        print(ex)
        return 'try again', 401

@auth.route('/login', methods=['POST'])
def signin() -> Union[Tuple[Response, int, Dict[str,str]], Response, Tuple[str, int]]:
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
                'auth_token': auth_token.decode('utf-8')
                }
            
                return jsonify(responseObj), 201, {'Content-Type': 'application/json'}
        else:
            return redirect("signup", code=303)
    
    except Exception as ex:
        print(ex)
        return 'try again', 401   


def validate_auth_token(func):
    """ Validate auth token """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({'message': 'A valid token is missing'}),
            401, {'Content-Type': 'application/json'})

        try:
            data = User.decode_auth_token(token)
            if isinstance(data, int):
                return func(*args, **kwargs)
            else:
                return make_response(jsonify({'message': data}),
                401, {'Content-Type': 'application/json'})
        except:
            return make_response(jsonify({'message': 'Token is invalid'}),
            401, {'Content-Type': 'application/json'})
    return decorated