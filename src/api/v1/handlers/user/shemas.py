from pydantic import BaseModel, EmailStr, Field

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


class OrderForm(BaseModel):
    fullName: str = Field(max_length=100)
    contact: str = Field(max_length=255)
    people: int = Field(ge=0)
    comments: str = Field(max_length=255)
    tour_id: int = Field(ge=0)
