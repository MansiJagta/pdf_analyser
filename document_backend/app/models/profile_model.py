from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
