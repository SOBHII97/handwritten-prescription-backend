from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import get_user_profile, get_prescription_history

user_bp = Blueprint('user', __name__)

user_bp.route('/profile', methods=['GET'])(jwt_required()(get_user_profile))
user_bp.route('/prescriptions', methods=['GET'])(jwt_required()(get_prescription_history))
