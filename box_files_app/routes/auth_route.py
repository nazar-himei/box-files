from flask import Blueprint, request, jsonify
from box_files_app.models.user_model import UserModel
from box_files_app.schemas.user_chema import UserSignUpBase, UserSignInBase
from box_files_app.controllers.user_controller import AuthController
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from box_files_app.app import (
    login_manager,
    login_user,
    logout_user,
    login_required,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


@auth.post('/sign_up')
def sign_up():
    try:
        data = UserSignUpBase.parse_raw(request.data)
        if not AuthController.valid_email(data.email) and not AuthController.valid_password(data.password):
            return jsonify({"message": "Invalid types"}), 400

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
        return jsonify({"message": "Invalid data of registration"})

    access_token = create_access_token(identity={"email": data.email})

    return jsonify({"status": "success", "access_token": access_token, "data": {
        "user": {"email": data.email, "first_name": data.first_name, "last_name": data.last_name}}}), 200


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    try:
        data = UserSignInBase.parse_raw(request.data)
        user = UserModel.query.filter_by(email=data.email).first()
        if not user:
            return jsonify({"message": "user empty"})

        valid_password = check_password_hash(pwhash=user.password_hash, password=data.password)

        if not valid_password:
            return jsonify({'message': "invalid user password"})
    except:
        return jsonify({"message": "Invalid data"})

    access_token = create_access_token(identity={"email": data.email})
    return jsonify({"status": "success", "access_token": access_token, "data": {
        "user": {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}}}), 200


@auth.route('/user/protected', methods=["GET", "POST"])
@jwt_required()
def protected_method():
    user = get_jwt_identity()
    return jsonify({"messages": "Secret data!", "access_token": user}), 200


@auth.route('/user/logout', methods=["GET", "POST"])
@login_required
@jwt_required()
def user_logout():
    logout_user()
