from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app.DB.config import mongo

@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
    return jsonify(user), 200

@jwt_required()
def get_prescription_history():
    user_id = get_jwt_identity()
    prescriptions = list(mongo.db.prescriptions.find({'user_id': ObjectId(user_id)}))
    for p in prescriptions:
        p['_id'] = str(p['_id'])  # convert ObjectId to string
        p['user_id'] = str(p['user_id'])
    return jsonify(prescriptions), 200
