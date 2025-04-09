from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.config import mongo  # متنساش تربطه في config.py

auth_bp = Blueprint('auth', __name__)

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(data['password'])

    user = {
        'email': data['email'],
        'password': hashed_password,
        'name': data.get('name'),
        'phone': data.get('phone')
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

#LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = mongo.db.users.find_one({'email': data['email']})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid password'}), 401
    
    # yrg3 JWT token lw successful login
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