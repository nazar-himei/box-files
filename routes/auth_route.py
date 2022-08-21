from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_login import (
    logout_user,
    login_required,
)

from application import login_manager
from consts.status_code import BADE_REQUEST_STATUS, UNSUPPORTED_TYPE_STATUS, OK_STATUS
from models.user_model import UserModel
from services.auth_service import AuthService
from services.token_service import TokenManager
from templates_json.auth_template_json import INVALID_TYPE_DATA_JSON, USER_ALREADY_JSON, USER_EMPTY_JSON, \
    INCORECT_DATA_USER

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@auth.route('/sign_up', methods=['POST'])
def sign_up():
    auth_service = AuthService(request=request)
    sign_up_base = auth_service.parse_sign_up_base()
    user_email = sign_up_base.email

    if sign_up_base is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS

    if auth_service.is_user_already_exists(email=user_email):
        return jsonify(USER_ALREADY_JSON), UNSUPPORTED_TYPE_STATUS

    auth_service.save_user_database()
    success_user_base = auth_service.get_auth_user_base(email=user_email)

    return jsonify(success_user_base.to_json()), OK_STATUS


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    auth_service = AuthService(request=request)
    sign_in_base = auth_service.parse_sign_in_base()
    user_email = sign_in_base.email

    if sign_in_base is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS

    if auth_service.is_user_already_exists(user_email):
        return jsonify(INCORECT_DATA_USER), UNSUPPORTED_TYPE_STATUS

    if not auth_service.is_valid_data_user():
        return jsonify(USER_EMPTY_JSON), UNSUPPORTED_TYPE_STATUS

    auth_service.update_status_active_user(email=user_email)
    success_user_base = auth_service.get_auth_user_base(email=user_email)

    return jsonify(success_user_base.to_json()), OK_STATUS


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth.route("/user/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    get_token = TokenManager.get_token(key=['email'])
    toke_manager = TokenManager(identity={"email": get_token})
    return jsonify(access_token=toke_manager.generate_token()), OK_STATUS


@auth.route('/user/logout', methods=["GET", "POST"])
@login_required
@jwt_required()
def user_logout():
    logout_user()
