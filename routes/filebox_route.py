from datetime import datetime
from io import BytesIO

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from application import login_manager, db
from consts.status_code import OK_STATUS, BADE_REQUEST_STATUS
from models.file_box_model import FileBoxModel
from models.user_model import UserModel
from services.file_box_service import FileBoxService
from services.file_manager import ZipFileManager
from templates_json.auth_template_json import INVALID_TYPE_OF_FILE, INVALID_TYPE_DATA_JSON, INVALID_FILE_ID

filebox = Blueprint('filebox', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@filebox.route('/filebox/files', methods=['GET', 'POST'])
@jwt_required()
def filebox_files():

    filebox_service = FileBoxService(request, get_jwt_identity()['email'])
    files = filebox_service.iterable_element_is_filebox()

    return jsonify({
        "status": "success",
        "data": files
    }), OK_STATUS


@filebox.route('/filebox/upload_file', methods=['POST'])
@jwt_required()
def upload_file():
    filebox_service = FileBoxService(request, get_jwt_identity()['email'])
    filebox_service.iterable_files_and_update_files_byte_context()

    if not filebox_service.is_valid_files():
        return jsonify(INVALID_TYPE_OF_FILE), BADE_REQUEST_STATUS

    filebox_service.upload_user_file()
    files = filebox_service.iterable_element_is_filebox()
    filebox_service.clean_file_bytes_context()

    return jsonify({
        "status": "success",
        "data": files
    }), OK_STATUS


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
            file_manger = ZipFileManager()

            for user_file in all_file.files:
                for data_id in files_id:
                    if user_file.id == data_id:
                        file_manger.write_file_to_zip(user_file.filename, user_file.data)

            file_manger.close_zip_file()
            return send_file(
                file_manger.file_byte,
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


@filebox.route('/filebox/deleteFile', methods=['GET', 'POST'])
@jwt_required()
def delete_file():
    filebox_service = FileBoxService(request, get_jwt_identity()['email'])
    files_scheme = filebox_service.parse_delete_file_scheme(request.data)

    if files_scheme is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS,

    files_id = files_scheme.files_id

    if filebox_service.is_empty_files_id(files_id):
        return jsonify(INVALID_FILE_ID), BADE_REQUEST_STATUS

    filebox_service.delete_file_from(files_id)
    files = filebox_service.iterable_element_is_filebox()

    return jsonify({"status": "success", "data": files}), OK_STATUS


@filebox.route('/filebox/updateFile', methods=['POST'])
@jwt_required()
def update_file():
    filebox_service = FileBoxService(request, get_jwt_identity()['email'])
    file_update_model = filebox_service.parse_update_file_model(request.data)

    if file_update_model is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS,

    if filebox_service.is_empty_files_id(file_update_model.id):
        return jsonify(INVALID_FILE_ID), BADE_REQUEST_STATUS

    filebox_service.update_file_model(file_update_model)
    files = filebox_service.iterable_element_is_filebox()

    return jsonify({"status": "success", "data": files}), OK_STATUS
