from flask import request, jsonify
from app.models.ai import segment_extract_text, enhance_text, extract_drugs_and_dosages
from PIL import Image
from datetime import datetime
from app.DB.config import mongo
from flask_jwt_extended import get_jwt_identity
from bson import ObjectId
from cerberus import Validator
from app.DB.SCHEMA.prescription_schema import prescription_schema

def upload_prescription():
    try:
        user_id = get_jwt_identity()
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        image = Image.open(file)

        extracted_text, segmented_image = segment_extract_text(image)
        enhanced_text = enhance_text(extracted_text)
        medications = extract_drugs_and_dosages(enhanced_text)

        prescription_data = {
    'user_id': str(user_id),
    'image_path': f"images/prescriptions/{file.filename}",
    'extracted_text': str(extracted_text),
    'corrected_text': str(enhanced_text),
    'medications': medications,
    'uploaded_at': str(datetime.utcnow())
        }


        validator = Validator(prescription_schema)
        if not validator.validate(prescription_data):
            return jsonify({'error': 'Invalid prescription data', 'details': validator.errors}), 400

        # convert user_id to ObjectId before insert
        prescription_data['user_id'] = ObjectId(user_id)

        mongo.db.prescriptions.insert_one(prescription_data)

        return jsonify({
            'message': 'Prescription uploaded successfully',
            'data': prescription_data
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
