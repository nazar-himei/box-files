from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from application import login_manager
from consts.status_code import OK_STATUS, BADE_REQUEST_STATUS
from models.user_model import UserModel
from services.file_box_service import FileBoxService
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
    filebox_service = FileBoxService(request, get_jwt_identity()['email'])
    files_scheme = filebox_service.parse_delete_file_scheme(request.data)

    if files_scheme is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS,

    files_id = files_scheme.files_id

    if filebox_service.is_empty_files_id(files_id):
        return jsonify(INVALID_FILE_ID), BADE_REQUEST_STATUS

    file_settings = filebox_service.generate_file_settings_model(files_id)
    return send_file(
        file_settings.file_byte,
        attachment_filename=file_settings.attachment_filename[0],
        mimetype=file_settings.mimetype,
        as_attachment=True
    )


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
