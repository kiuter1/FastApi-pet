from pydantic import BaseModel

class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class RegistrationForm(BaseModel):
    username: str
    password: str
    email: str


class LoginForm(BaseModel):
    username: str
    password: str
