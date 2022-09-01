from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_login import (
    logout_user,
    login_required,
)

from application import login_manager
from consts.status_code import BADE_REQUEST_STATUS, UNSUPPORTED_TYPE_STATUS, OK_STATUS
from consts.templates_json.auth_template_json import (
    USER_ALREADY_JSON,
    USER_EMPTY_JSON,
    INCORRECT_DATA_USER,
)
from consts.templates_json.filebox_template_json import INVALID_TYPE_DATA_JSON
from models.user_model import UserModel
from services.auth_service import AuthService
from services.token_service import TokenService

auth = Blueprint(
    'auth',
    __name__,
    url_prefix="/api/v1/",
)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@auth.route('/register', methods=['POST'])
def register():
    auth_service = AuthService(request=request)
    sign_up_base = auth_service.parse_sign_up_base()

    if sign_up_base is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS

    user_email = sign_up_base.email

    if auth_service.is_user_already_exists(email=user_email):
        return jsonify(USER_ALREADY_JSON[0]), UNSUPPORTED_TYPE_STATUS

    auth_service.save_user_database()
    auth_user_base = auth_service.get_auth_user_base(email=user_email)

    return jsonify(auth_user_base.to_json()), OK_STATUS


@auth.route('/login', methods=['POST'])
def login():
    auth_service = AuthService(request=request)
    sign_in_base = auth_service.parse_sign_in_base()

    if sign_in_base is None:
        return jsonify(INVALID_TYPE_DATA_JSON), BADE_REQUEST_STATUS

    user_email = sign_in_base.email

    if not auth_service.is_user_already_exists(user_email):
        return jsonify(USER_EMPTY_JSON), UNSUPPORTED_TYPE_STATUS

    if not auth_service.is_valid_data_user():
        return jsonify(INCORRECT_DATA_USER), UNSUPPORTED_TYPE_STATUS

    auth_service.update_status_active_user(email=user_email)
    auth_user_base = auth_service.get_auth_user_base(email=user_email)

    return jsonify(auth_user_base.to_json()), OK_STATUS


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth.route("/refreshToken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    get_info_token = TokenService.get_token(key="email")
    toke_manager = TokenService(identity={"email": get_info_token})

    return jsonify(
        access_token=toke_manager.generate_token(),
        refresh_token=toke_manager.generate_refresh_token()
    ), OK_STATUS


@auth.route('/logOut', methods=["POST"])
@login_required
@jwt_required()
def user_logout():
    logout_user()
