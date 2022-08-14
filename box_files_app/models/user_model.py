from box_files_app.app import db
from flask_login import UserMixin
from datetime import datetime


class UserModel(UserMixin, db.Model):
    """User model"""

    __tablename__ = "user"

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password
        self.created_on = datetime.utcnow()

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(150))
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=False)
