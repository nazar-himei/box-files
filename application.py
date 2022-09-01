from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from configs.dev_config import DevConfig
from extensions.exception_extension import register_exception_handler
from extensions.flask_config_extension import flask_config
from extensions.routes_extensions import register_routes

db = SQLAlchemy()
jwt_manager = JWTManager()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    flask_config(app, DevConfig())
    register_routes(app)
    register_exception_handler(app)
    db.init_app(app)

    with app.app_context():
        if db.app is None:
            from services.session_service import SessionService

            SessionService.create_db()

    jwt_manager.init_app(app)
    login_manager.init_app(app)

    return app
