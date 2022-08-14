from box_files_app.regexps import email_regex, password_regex
from werkzeug.security import generate_password_hash, check_password_hash
from box_files_app.app import db
from box_files_app.models.user_model import UserModel
import re


class AuthController:

    def __init__(self, user_model=None, user_base=None):
        self.user_model = user_model
        self.user_base = user_base

    @staticmethod
    def is_valid_value(validation_value, regex_patter):
        value_regex = re.compile(regex_patter)

        if not re.match(value_regex, validation_value):
            return False
        return True

    @staticmethod
    def valid_email(email):
        return AuthController.is_valid_value(email, email_regex)

    @staticmethod
    def valid_password(password):
        return AuthController.is_valid_value(password, password_regex)

    def find_by_user_database(self):
        assert (self.user_model is not None, "UserModel most not null")

        return UserModel.query.filter_by(email=self.user_base.email)

    def save_user_database(self):
        assert (self.user_model is not None, "UserModel most not null")
        db.create_all()
        self.hash_password(self.user_model.password_hash)
        db.session.add(self.user_model)
        db.session.commit()

    def delete_user_database(self):
        assert (self.user_model is not None, "UserModel most not null")

        self.find_by_user_database().delete()

    def hash_password(self, password):
        assert (self.user_model is not None, "UserModel most not null")

        self.user_model.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        assert (self.user_model is not None, "UserModel most not null")

        return check_password_hash(self.user_model.password_hash, password)
