from box_files_app.app import db
from datetime import datetime


class FileBoxModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    datetime_file = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    file_id = db.Column(db.Integer, db.ForeignKey('all_file_model.id'))


class AllFileModel(db.Model):
    __tablename__ = "all_file_model"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    files = db.relationship('FileBoxModel', backref='all_file_model', lazy=True)
