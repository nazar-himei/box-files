import base64
from io import BytesIO

import magic
from flask import Blueprint, request, jsonify, send_file

from box_files_app.app import db, login_manager
from box_files_app.models.file_box_model import FileUserModel, FileBoxModel
from box_files_app.models.user_model import UserModel

filebox = Blueprint('filebox', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@filebox.route('/filebox/files', methods=['GET'])
def get_files():
    user_id = 1
    all_file = FileBoxModel.query.filter_by(user_id=user_id).first()
    user_files = []

    if all_file is not None:
        for file in all_file.files:
            file_json = {
                "filename": file.filename,
                "create_file": file.created_file_time.isoformat(),
                "changed_file": file.changed_file_time.isoformat(),
                "size_data": file.size_of_data,
                "type_data": file.type_of_data,
                "id": file.id
            }
            user_files.append(file_json)

    return jsonify({"status": "success", "data": user_files})


@filebox.route('/filebox/upload_file', methods=['POST'])
def upload_file():
    # Clean database.
    # db.drop_all()
    # db.create_all()

    data_file = request.files['file']
    read_file = data_file.read()

    # encode / decode file
    image_string_encode = base64.b64encode(read_file)
    image_string_decode = base64.b64decode(image_string_encode)

    # get type file from base64
    bytes_file = BytesIO(image_string_decode)
    bytes_file.seek(0)
    type_file = magic.from_buffer(bytes_file.read(), mime=True).split('/')[-1]

    # parse size of file
    file_size = len(image_string_encode) * 3 / 4 - str(image_string_encode).count('=')

    user_files = FileBoxModel.query.filter_by(user_id=1).first()
    if user_files is None:
        # Create model for database.
        file_box = FileBoxModel(user_id=1)
        file_user = FileUserModel(
            filename=data_file.filename,
            data=read_file,
            size_of_data=file_size,
            type_of_data=type_file,
        )
        file_box.files.append(file_user)
        db.session.add(file_box)
        db.session.commit()

        return jsonify({"status": "success", "filename": file_user.filename, "size_file": 1})

    # Get currency model from database.
    file_box = FileBoxModel.query.filter_by(user_id=1)[0]
    file_user = FileUserModel(
        filename=data_file.filename,
        data=read_file,
        data_base64=image_string_encode,
        size_of_data=file_size,
        type_of_data=type_file,
        file_key=file_box.id
    )
    db.session.add(file_user)
    db.session.commit()

    return jsonify({"status": "success", "filename": data_file.filename, "size_file": 1})


@filebox.route('/filebox/download_file', methods=['GET', 'POST'])
def download_file():
    file_id = request.json['id']
    user_id = 1
    all_file = FileBoxModel.query.filter_by(user_id=user_id).first()

    for file in all_file.files:
        if file.id == file_id:
            return send_file(BytesIO(file.data), attachment_filename=file.filename, as_attachment=True)

    return jsonify({"status": "fail", "messages": "invalid id file"})


@filebox.route('/filebox/delete_file', methods=['GET', 'POST'])
def delete_file():
    id_file = request.json['file_id']
    user_id = 1
    all_file = FileBoxModel.query.filter_by(user_id=user_id).first()
    if all_file is None:
        return jsonify({"status": "fail", 'message': 'invalid id file'})
    for file in all_file.files:
        if file.id == id_file:
            db.session.delete(file)
            db.session.commit()

    user_files = []
    if all_file is not None:
        for file in all_file.files:
            print()
            file_json = {
                "filename": file.filename,
                "create_file": file.created_file_time.isoformat(),
                "id": file.id
            }
            user_files.append(file_json)

    return jsonify({"status": "success", "data": user_files})


@filebox.route('/filebox/update_file', methods=['POST'])
def update_file():
    id_file = request.json['id']
    filename = request.json['filename']
    user_id = 1
    all_file = FileBoxModel.query.filter_by(user_id=user_id).first()
    if all_file is None:
        return jsonify({"status": "fail", 'message': 'invalid id file'})

    file = all_file.files[0]
    file.filename = filename
    db.session.commit()

    return jsonify({"status": "fail", 'message': 'invalid id file'})
