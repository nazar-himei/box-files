from io import BytesIO
from flask import Blueprint, request, jsonify, send_file
from box_files_app.app import db, login_manager
from box_files_app.models.user_model import UserModel
from box_files_app.models.file_box_model import FileBoxModel, AllFileModel

filebox = Blueprint('filebox', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@filebox.route('/filebox/get_files', methods=['GET'])
def get_files():
    user_id = 1
    all_file = AllFileModel.query.filter_by(user_id=user_id).first()
    user_files = []

    if all_file is not None:
        for file in all_file.files:
            print(file)
            file_json = {
                "filename": file.filename, "create_file": file.datetime_file, "file_id": file.id
            }
            user_files.append(file_json)

    print(user_files)
    return jsonify({"status": "success", "data": f"{user_files}"})


@filebox.route('/filebox/upload_file', methods=['POST'])
def upload_file():
    # Clean database.
    # db.drop_all()
    # db.create_all()

    file = request.files['file']
    user_files = AllFileModel.query.filter_by(user_id=1)
    if user_files.first() is None:
        # Create model for database.
        print("MODEL EMPTY")
        all_file = AllFileModel(user_id=1)
        file_box = FileBoxModel(filename=file.filename, data=file.read())
        all_file.files.append(file_box)
        db.session.add(all_file)
        db.session.commit()
        print(AllFileModel.query.filter_by(user_id=1).first().files)

        return jsonify({"status": "success", "filename": file_box.filename, "size_file": 1})
    # Get currency model from database.
    all_file = AllFileModel.query.filter_by(user_id=1)[0]
    filex_box = FileBoxModel(filename=file.filename, data=file.read(), file_id=all_file.id)
    db.session.add(filex_box)
    db.session.commit()
    print(f"RESULT {all_file.files}")
    return jsonify({"status": "success", "filename": file.filename, "size_file": 1})


@filebox.route('/filebox/download_file', methods=['GET', 'POST'])
def download_file():
    file_id = request.json['file_id']
    user_id = 1
    all_file = AllFileModel.query.filter_by(user_id=user_id).first()
    file_box = all_file.files[0]

    for file in all_file.files:
        if file.id == file_id:
            file_box = file

    if all_file is None or file_box is None:
        return jsonify({"status": "fail", "messages": "invalid id file"})

    return send_file(BytesIO(file_box.data), attachment_filename=file_box.filename, as_attachment=True)
#
#
# @filebox.route('/filebox/delete_file', methods=['GET', 'POST'])
# def delete_file():
#     file = request.files['file']
#     db.create_all()
#     upload_model = FileModel.query.filter_by(filename=file).first()
#     upload_model.delete()
#     db.session.add(upload_model)
#     db.session.commit()
#
#     return jsonify({"status": "success", "filename": file.filename})
