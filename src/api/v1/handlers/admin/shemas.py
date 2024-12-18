from pydantic import BaseModel, Field
from typing import Optional


class TourForm(BaseModel):
    name: str = Field(max_length=50)
    location: str = Field(max_length=200)
    description: str
    price: float = Field(ge=0)
    photo: Optional[bytes] = None

