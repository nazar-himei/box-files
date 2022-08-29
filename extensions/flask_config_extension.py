import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv('.env')


def flask_config(app):
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=12)


def flask_run(app):
    flask_is_prod = os.getenv("FLASK_CONTROL_VERSION") == ("dev", "develop")
    host = os.getenv("FLASK_RUN_HOST")
    port = os.getenv("FLASK_RUN_PORT")
    app.run(
        debug=flask_is_prod,
        host=host,
        port=port,
    )
