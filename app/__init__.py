from flask import Flask
from flask_cors import CORS
<<<<<<< HEAD
from flask_jwt_extended import JWTManager
from app.routes.auth_route import auth_bp
from app.routes.user import user_bp
from app.routes.prescription_routes import prescription_bp
from app.routes.ai_route import ai_bp
from app.DB.config import Config, mongo

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    mongo.init_app(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(prescription_bp, url_prefix='/api/prescription')
    app.register_blueprint(ai_bp, url_prefix='/process')

    return app
=======
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
>>>>>>> 02b84f9da85646972988ab87e03fa562539deb0a
