# from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
# from sqlalchemy.orm import relationship
# from app.models.profile_model import Base

# class Document(Base):
#     __tablename__ = "document"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     profile_id = Column(Integer, ForeignKey("profile.id"), nullable=True)
#     filename = Column(String, nullable=False)
#     path = Column(String, nullable=False)
#     file_type = Column(String, nullable=False)      # 'pdf', 'image', 'scan'
#     size_kb = Column(Integer, nullable=True)
#     num_pages = Column(Integer, nullable=True)
#     language = Column(String, nullable=True)       # e.g., 'en'
#     hash = Column(String, nullable=True)           # for deduplication
#     status = Column(String, nullable=False, default="uploaded")  # 'uploaded', 'extracted', 'summarized'
#     upload_time = Column(TIMESTAMP, server_default=func.current_timestamp())
#     last_processed = Column(TIMESTAMP, nullable=True)

#     profile = relationship("Profile", backref="documents")
# app/models/document_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    size_kb = Column(Integer, nullable=True)
    num_pages = Column(Integer, nullable=True)
    language = Column(String, nullable=True)
    hash = Column(String, nullable=True)
    status = Column(String, nullable=False, default="uploaded")
    upload_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    last_processed = Column(TIMESTAMP, nullable=True)

    profile = relationship("Profile", backref="documents")
