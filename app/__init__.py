from flask import Flask
from flask_cors import CORS
from app.routes.auth import auth_bp
from app.config import Config, mongo
from flask_jwt_extended import JWTManager
from app.routes.ai import ai_bp

def create_app():
    app = Flask(__name__)
    CORS(app) 
    app.config.from_object(Config)
    mongo.init_app(app)
    JWTManager(app)
   
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    return app