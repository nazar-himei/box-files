from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,

)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from box_files_app.app import (
    login_manager,
    login_user,
    logout_user,
    login_required,
)
from box_files_app.controllers.user_controller import AuthController
from box_files_app.models.user_model import UserModel
from box_files_app.schemas.user_chema import UserSignUpBase, UserSignInBase

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@auth.post('/sign_up')
def sign_up():
    try:
        data = UserSignUpBase.parse_raw(request.data)
        if not AuthController.valid_email(data.email) and not AuthController.valid_password(data.password):
            return jsonify({"message": "Invalid types data"}), 400

        user_model = UserModel(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password,
        )
        auth_controller = AuthController(user_model, data)
        auth_controller.save_user_database()
        login_user(user_model)

    except IntegrityError:
        return jsonify({"message": "User Already Exists"}), 400

    except:
        return jsonify({"message": "Invalid data of registration"}), 415

    access_token = create_access_token(identity={"email": data.email})
    refresh_token = create_refresh_token(identity={"email": data.email})
    return jsonify({"status": "success", "access_token": access_token, "refresh_token": refresh_token, "data": {
        "user": {"email": data.email, "first_name": data.first_name, "last_name": data.last_name}}}), 200


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    try:
        data = UserSignInBase.parse_raw(request.data)
        user = UserModel.query.filter_by(email=data.email).first()
        valid_password = check_password_hash(pwhash=user.password_hash, password=data.password)

        if not user or not valid_password:
            return jsonify({"status": "fail", "message": "invalid data of user"})

    except:
        return jsonify({"message": "Invalid types data"}), 415

    access_token = create_access_token(identity={"email": data.email})
    refresh_token = create_refresh_token(identity={"email": data.email})

    return jsonify({"status": "success", "access_token": access_token, "refresh_token": refresh_token, "data": {
        "user": {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}}}), 200


@auth.route('/user/protected', methods=["GET", "POST"])
@jwt_required()
def protected_method():
    user = get_jwt_identity()
    return jsonify({"messages": "Secret data!", "access_token": user['email']}), 200


@auth.route('/user/logout', methods=["GET", "POST"])
@login_required
@jwt_required()
def user_logout():
    logout_user()


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth.route("/user/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()['email']
    access_token = create_access_token(identity={"email": identity})
    return jsonify(access_token=access_token)
