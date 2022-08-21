import os

from base_config import BaseConfig


class ProductionConfig(BaseConfig):
    """Flask config class."""

    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
