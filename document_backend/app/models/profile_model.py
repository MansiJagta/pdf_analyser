from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.database import Base
from app.models.base import Base

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())