from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from extensions.exception_extension import register_exception_handler
from extensions.routes_extensions import register_routes

db = SQLAlchemy()
jwt_manager = JWTManager()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    register_routes(app)
    register_exception_handler(app)
    db.init_app(app)
    jwt_manager.init_app(app)
    login_manager.init_app(app)

    return app
