from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.prescription_controller import upload_prescription

prescription_bp = Blueprint('prescription', __name__)

prescription_bp.route('/upload', methods=['POST'])(jwt_required()(upload_prescription))
