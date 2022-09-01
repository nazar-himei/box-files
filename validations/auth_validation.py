import re

from werkzeug.security import check_password_hash

from validations.regexps import EMAIL_REGEX, PASSWORD_REGEX


class AuthValidation:
    @staticmethod
    def is_valid_value(validation_value, regex_patter):
        value_regex = re.compile(regex_patter)

        if not re.match(value_regex, validation_value):
            return False
        return True

    @staticmethod
    def valid_email(email):
        return AuthValidation.is_valid_value(email, EMAIL_REGEX)

    @staticmethod
    def valid_password(password):
        return AuthValidation.is_valid_value(password, PASSWORD_REGEX)

    @staticmethod
    def valid_password_and_email(email, password):
        return AuthValidation.valid_email(email) and AuthValidation.valid_password(password)

    @staticmethod
    def verify_password(password, password_hash):
        return check_password_hash(password_hash, password)
