from pydantic.error_wrappers import ValidationError
from werkzeug.security import generate_password_hash

from models.user_model import UserModel
from repositories.profile_repository import ProfileRepository
from schemas.auth_schema import UserSignUpBase, UserSignInBase, AuthUserBase
from services.token_service import TokenService
from validations.auth_validation import AuthValidation


class AuthService:
    """
    Auth Service has function for work with authentication.
    """

    def __init__(self, request=None):
        self.request = request

    # Get information about user from repository
    @staticmethod
    def get_user(email):
        return ProfileRepository.get_user(user_email=email)

    # Updated status user if user login or registration in system
    @staticmethod
    def update_status_active_user(email):
        ProfileRepository.update_status_active_user(email)

    # Save information about user to storage
    def save_user_database(self):
        sign_in_base = self.parse_sign_in_base()
        if sign_in_base is None:
            return

        user_model = self.generate_user_model()
        ProfileRepository.add_user(user_model=user_model)

    # Delete user from storage
    @staticmethod
    def delete_user_db(user_id):
        user = ProfileRepository.get_user(user_id)
        if user is None:
            return

        ProfileRepository.delete_user(user)

    # Generate user model for send response
    def generate_user_model(self):
        base_model = self.parse_sign_up_base()
        if base_model is None:
            return

        return UserModel(
            first_name=base_model.first_name,
            last_name=base_model.last_name,
            email=base_model.email,
            password=self.hash_password(base_model.password),
        )

    def parse_sign_in_base(self):
        try:
            data = UserSignInBase.parse_raw(self.request.data)
        except ValidationError:
            return None

        return data

    def parse_sign_up_base(self):
        try:
            data = UserSignUpBase.parse_raw(self.request.data)
        except ValidationError:
            return None

        return data

    # Check user email already in the system
    @staticmethod
    def is_user_already_exists(email):
        user = ProfileRepository.get_user(user_email=email)

        if user is None:
            return False

        return True

    # Generate hash password
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    # Get token service
    @staticmethod
    def token_manager(email):
        return TokenService(identity={"email": email})

    # User data validation
    def is_valid_data_user(self):
        user_base = self.parse_sign_in_base()
        user_model = self.get_user(email=user_base.email)
        if user_model is None:
            return False

        valid_password = AuthValidation.verify_password(
            password=user_base.password,
            password_hash=user_model.password_hash,
        )
        return valid_password

    # Get user model for send response
    def get_auth_user_base(self, email):
        token_manager = self.token_manager(email=email)

        return AuthUserBase(
            user_model=self.get_user(email=email),
            access_token=token_manager.generate_token(),
            refresh_token=token_manager.generate_refresh_token(),
        )
