from datetime import datetime

prescription_schema = {
    "user_id": {"type": "string", "required": True},
    "image_path": {"type": "string", "required": True},
    "extracted_text": {"type": "string", "required": False},
    "corrected_text": {"type": "string", "required": False},
    "uploaded_at": {"type": "string", "required": False},
    "medications": {"type": "list", "required": False}
}
