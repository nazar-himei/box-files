from base64 import b64encode, b64decode
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from magic import from_buffer

from box_files_app.app import db, login_manager
from box_files_app.models.file_box_model import FileUserModel, FileBoxModel
from box_files_app.models.user_model import UserModel

filebox = Blueprint('filebox', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@filebox.route('/filebox/files', methods=['GET'])
@jwt_required()
def filebox_files():
    jwt_email_user = get_jwt_identity()['email']
    user = UserModel.query.filter_by(email=jwt_email_user).first()
    all_file = FileBoxModel.query.filter_by(user_id=user.id).first()

    if all_file is None:
        return jsonify({"status": "success", "data": []})

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
@jwt_required()
def upload_file():
    # Clean database.
    # db.drop_all()
    # db.create_all()

    data_file = request.files['file']
    read_file = data_file.read()

    user_email = get_jwt_identity()['email']
    user = UserModel.query.filter_by(email=user_email).first()

    # encode / decode file
    image_string_encode = b64encode(read_file)
    image_string_decode = b64decode(image_string_encode)

    # get type file from base64
    bytes_file = BytesIO(image_string_decode)
    bytes_file.seek(0)
    type_file = from_buffer(bytes_file.read(), mime=True).split('/')[-1]

    # parse size of file
    file_size = len(image_string_encode) * 3 / 4 - str(image_string_encode).count('=')

    user_files = FileBoxModel.query.filter_by(user_id=user.id).first()

    if user_files is None:
        # Create model for database.
        file_box = FileBoxModel(user_id=user.id)
        file_user = FileUserModel(
            filename=data_file.filename,
            data=read_file,
            size_of_data=file_size,
            type_of_data=type_file,
        )
        file_box.files.append(file_user)
        db.session.add(file_box)
        db.session.commit()

        return jsonify({"status": "success", "filename": file_user.filename, "size_file": 1}), 200

    # Get currency model from database.
    file_box = FileBoxModel.query.filter_by(user_id=user.id)[0]
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
@jwt_required()
def downloads_file():
    files_id = request.json['files_id']

    user_email = get_jwt_identity()['email']
    user = UserModel.query.filter_by(email=user_email).first()
    all_file = FileBoxModel.query.filter_by(user_id=user.id).first()

    if all_file is None:
        return jsonify({"status": "fail", "messages": "data is empty"})

    try:
        if len(files_id) > 1:
            file_byte = BytesIO()
            zip_file = ZipFile(file_byte, 'w', ZIP_DEFLATED)

            for user_file in all_file.files:
                for data_id in files_id:
                    if user_file.id == data_id:
                        zip_file.writestr(user_file.filename, user_file.data)

            zip_file.close()
            file_byte.seek(0)
            return send_file(
                file_byte,
                attachment_filename=f'filebox-download-{datetime.utcnow().isoformat()}.zip',
                mimetype="application/zip",
                as_attachment=True,
            )

        for file in all_file.files:
            if file.id == files_id[0]:
                return send_file(
                    BytesIO(file.data),
                    attachment_filename=file.filename,
                    mimetype=f"application/{file.type_of_data}",
                    as_attachment=True,
                )
    except TypeError:
        return jsonify({"status": "failed", "messages": "invalid type file"}), 502

    return jsonify({"status": "fail", "messages": "invalid id file"})


@filebox.route('/filebox/delete_file', methods=['GET', 'POST'])
@jwt_required()
def delete_file():
    files_id = request.json['files_id']

    user_email = get_jwt_identity()['email']
    user = UserModel.query.filter_by(email=user_email).first()

    all_file = FileBoxModel.query.filter_by(user_id=user.id).first()
    if all_file is None:
        return jsonify({"status": "fail", 'message': 'invalid id file'})

    try:
        for file in all_file.files:
            for data_id in files_id:
                if file.id == data_id:
                    db.session.delete(file)
                    db.session.commit()
    except TypeError:
        return jsonify({"status": "failed", "messages": "invalid type file"}), 502

    user_files = []
    if all_file is not None:
        for file in all_file.files:
            file_json = {
                "filename": file.filename,
                "create_file": file.created_file_time.isoformat(),
                "id": file.id
            }
            user_files.append(file_json)

    return jsonify({"status": "success", "data": user_files})


@filebox.route('/filebox/update_file', methods=['POST'])
@jwt_required()
def update_file():
    id_file = request.json['id']
    filename = request.json['filename']

    user_email = get_jwt_identity()['email']
    user = UserModel.query.filter_by(email=user_email).first()

    all_file = FileBoxModel.query.filter_by(user_id=user.id).first()

    if all_file is None:
        return jsonify({"status": "fail", 'message': 'data is empty'})

    for file in all_file.files:

        if id_file == file.id:
            file.filename = filename
            db.session.commit()

            return jsonify({"status": "success"})

    return jsonify({"status": "fail", "msg": "Invalid id file"})
