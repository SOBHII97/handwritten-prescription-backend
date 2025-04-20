from flask import Blueprint, request, send_file, jsonify
from PIL import Image
import io
import base64
from app.models.ai import segment_text_lines, segment_extract_text, extract_drugs_and_dosages

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/process_text', methods=['POST'])
def process_original():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    medications = extract_drugs_and_dosages(text)
    if medications:
        return jsonify(medications)
    else:
        return jsonify({"error": "No medications detected"}), 400

@ai_bp.route('/segmentation', methods=['POST'])
def process_segmentation():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img = Image.open(file.stream)
    segmented_img = segment_text_lines(img)

    output = io.BytesIO()
    segmented_img.save(output, format='JPEG')
    output.seek(0)

    return send_file(output, mimetype='image/jpeg')

@ai_bp.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img = Image.open(file.stream)
    text, segmented_img = segment_extract_text(img)

    output = io.BytesIO()
    segmented_img.save(output, format='JPEG')
    output.seek(0)
    img_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

    return jsonify({
        'text': text,
        'segmented_image': img_base64
    })
