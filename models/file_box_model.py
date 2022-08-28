from application import db
from datetime import datetime


class FileUserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    data = db.Column(db.LargeBinary)
    data_base64 = db.Column(db.TEXT, nullable=True)
    created_file_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    changed_file_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    size_of_data = db.Column(db.Float)
    type_of_data = db.Column(db.String(20), nullable=True)
    file_key = db.Column(db.Integer, db.ForeignKey('file_box_model.id'))


class FileBoxModel(db.Model):
    __tablename__ = "file_box_model"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    files = db.relationship('FileUserModel', backref='file_box_model', lazy=True)
