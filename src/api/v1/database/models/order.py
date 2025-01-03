from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.api.v1.database.base import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    contact = Column(String(255), nullable=False)
    persons = Column(Integer, nullable=False)
    comments = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tour_id = Column(Integer, ForeignKey('tour.id'), nullable=False)
    user = relationship("User", backref="orders")
    tour = relationship("Tour", backref="orders")