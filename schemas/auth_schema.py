from pydantic import BaseModel


class UserSignUpBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str

    def __repr__(self):
        return f'email {self.email} first_name: {self.first_name}, last_name: {self.last_name}  password {self.password}'


class UserSignInBase(BaseModel):
    email: str
    password: str

    def __repr__(self):
        return f'email {self.email} password {self.password}'


class AuthUserBase:
    def __init__(self, user_model, access_token, refresh_token):
        self.user_model = user_model
        self.access_token = access_token
        self.refresh_token = refresh_token

    def to_json(self):
        return {
            "status": "success",
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "data": {
                "email": self.user_model.email,
                "first_name": self.user_model.first_name,
                "last_name": self.user_model.last_name,
            }}
