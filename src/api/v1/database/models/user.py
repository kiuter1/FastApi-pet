from sqlalchemy import Column, String, Integer, Boolean, LargeBinary

from src.api.v1.database.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)