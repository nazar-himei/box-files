from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask_jwt_extended import JWTManager


app = Flask(__name__)
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager(app)


def create_app():
    from routes.auth_route import auth
    app.register_blueprint(auth)
    from routes.filebox_route import filebox
    app.register_blueprint(filebox)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
