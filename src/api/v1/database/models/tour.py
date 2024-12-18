from sqlalchemy import Column, String, Integer, Text, Float
from sqlalchemy.orm import relationship

from src.api.v1.database.base import Base


class Tour(Base):
    __tablename__ = "tour"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    location = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    photo = relationship('Photo', back_populates='tour', cascade='all, delete-orphan')