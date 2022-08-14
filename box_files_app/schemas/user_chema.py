from pydantic import BaseModel, root_validator, validator


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
