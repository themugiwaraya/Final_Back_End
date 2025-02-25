from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = Config.MONGO_URI
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app
