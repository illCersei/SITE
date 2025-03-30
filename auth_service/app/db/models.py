from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, VARCHAR

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(VARCHAR, unique=True, nullable=False)
    password = Column(VARCHAR, nullable=False)
