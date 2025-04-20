from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.auth_controller import register_controller, login_controller, logout_controller

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(register_controller)
auth_bp.route('/login', methods=['POST'])(login_controller)
auth_bp.route('/logout', methods=['POST'])(jwt_required()(logout_controller))
