import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from src.api.v1.database.base import Base


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tour_id = Column(Integer, ForeignKey('tour.id', ondelete='CASCADE'))
    url = Column(Text, nullable=False)
    filename = Column(String(255), nullable=False)
    url_updated = Column(BigInteger, nullable=False, default=int(datetime.datetime.now().timestamp()))
    tour = relationship('Tour', back_populates='photo')