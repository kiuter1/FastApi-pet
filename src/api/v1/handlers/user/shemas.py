from pydantic import BaseModel, EmailStr

class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class RegistrationForm(BaseModel):
    username: str
    password: str
    email: EmailStr


class LoginForm(BaseModel):
    username: str
    password: str
