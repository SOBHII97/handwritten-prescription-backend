from datetime import timedelta
from flask_pymongo import PyMongo

mongo = PyMongo()

class Config:
    MONGO_URI = "mongodb://localhost:27017/prescription_db"
    JWT_SECRET_KEY = "secretkey123"   
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) 