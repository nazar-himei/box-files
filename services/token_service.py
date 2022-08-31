from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_current_user,
)


class TokenService:
    """Token Service provide function for work with token"""

    def __init__(self, identity):
        self.identity = identity

    # Get encode value from token
    @staticmethod
    def get_token(key):
        token = get_jwt_identity()
        if key is None:
            return token

        return get_jwt_identity()[key]

    # Get current user
    @staticmethod
    def current_user():
        return get_current_user()

    # Generate token for user
    def generate_token(self):
        return create_access_token(identity=self.identity)

    # Generate refresh token for user
    def generate_refresh_token(self):
        return create_refresh_token(identity=self.identity)
