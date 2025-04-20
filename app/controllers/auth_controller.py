from flask import request, jsonify, Blueprint 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.DB.config import mongo
from cerberus import Validator
from app.DB.SCHEMA.user_schema import user_schema
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    validator = Validator(user_schema)
    if not validator.validate(data):
        return jsonify({'error': 'Validation failed', 'details': validator.errors}), 400

    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(data['password'])

    user = {
        'email': data['email'],
        'password': hashed_password,
        'name': data['name'],
        'phone': data.get('phone'),
        'profile_picture': data.get('profile_picture'),
        'created_at': str(datetime.utcnow()),
        'updated_at': str(datetime.utcnow())
    }

    mongo.db.users.insert_one(user)

    return jsonify({
        'message': 'Registration successful',
        'user': {
            'email': user['email'],
            'name': user['name'],
            'phone': user['phone']
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login_controller():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = mongo.db.users.find_one({'email': data['email']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'email': user['email'],
            'name': user.get('name'),
            'phone': user.get('phone')
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_controller():
    return jsonify({'message': 'Logged out successfully (Client should discard token)'}), 200
