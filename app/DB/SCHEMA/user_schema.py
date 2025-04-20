from datetime import datetime


# User Schema with validation and optional fields

user_schema = {
    "email": {
        "type": "string",  
        "required": True,
        "regex": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    },
    "password": {
        "type": "string",
        "required": True,
        "regex": r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$"
    },
    "name": {
        "type": "string",
        "required": True
    },
    "phone": {
        "type": "string",
        "required": False
    },
    "profile_picture": {
        "type": "string",
        "required": False
    },
    "created_at": {
        "type": "string",  
        "required": False
    },
    "updated_at": {
        "type": "string",
        "required": False
    }
}
