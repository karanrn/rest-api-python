from flask import jsonify
from typing import Dict

# Custom Error Helper Functions
def bad_request(message: str) -> Dict[str, str]:
    response = jsonify({'error': message})
    response.status_code = 400
    return response

def not_found(message:str) -> Dict[str, str]:
    response = jsonify({'error': message})
    response.status_code = 404
    return response