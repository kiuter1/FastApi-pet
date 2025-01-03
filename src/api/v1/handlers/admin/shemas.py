from pydantic import BaseModel, Field
from typing import Optional


class TourForm(BaseModel):
    id: int = None
    name: str = Field(max_length=50)
    location: str = Field(max_length=200)
    description: str
    price: float = Field(ge=0)
    photo: object = None
    photo_name: str = Field(max_length=255, default=None)
    photo_url: str = None


class DelTourForm(BaseModel):
    id: int = Field(ge=0)


class UserChangeForm(BaseModel):
    id: int = None
    is_admin: bool = Field(default=False)


class OrderChangeForm(BaseModel):
    id: int = None
    is_done: bool = Field(default=False)

class DelOrderForm(BaseModel):
    id: int = Field(ge=0)