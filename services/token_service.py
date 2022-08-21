from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_current_user,
)


class TokenManager:
    def __init__(self, identity):
        self.identity = identity

    @staticmethod
    def get_token(key):
        token = get_jwt_identity()
        if key in None:
            return token

        return get_jwt_identity()[key]

    @staticmethod
    def current_user():
        return get_current_user()

    def generate_token(self):
        return create_access_token(identity=self.identity)

    def generate_refresh_token(self):
        return create_refresh_token(identity=self.identity)
