import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv('.env')


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    HOST = os.getenv("FLASK_RUN_HOST")
    PORT = os.getenv("FLASK_RUN_PORT")
    FLASK_CONTROL_VERSION = os.getenv("FLASK_CONTROL_VERSION")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)
