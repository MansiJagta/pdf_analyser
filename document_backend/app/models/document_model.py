# # from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func, Text
# # from sqlalchemy.orm import relationship
# # from app.models.base import Base


# # class Document(Base):
# #     __tablename__ = "document"

# #     id = Column(Integer, primary_key=True, autoincrement=True)
# #     profile_id = Column(Integer, ForeignKey("profile.id"), nullable=True)

# #     filename = Column(String, nullable=False)
# #     path = Column(String, nullable=False)
# #     file_type = Column(String, nullable=False)
# #     size_kb = Column(Integer, nullable=True)

# #     num_pages = Column(Integer, nullable=True)
# #     language = Column(String, nullable=True)
# #     hash = Column(String, nullable=True)

# #     status = Column(String, nullable=False, default="uploaded")
# #     error_message = Column(Text, nullable=True)

# #     upload_time = Column(TIMESTAMP, server_default=func.current_timestamp())
# #     last_processed = Column(TIMESTAMP, nullable=True)

# #     profile = relationship("Profile")






# from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func, Text
# from sqlalchemy.orm import relationship
# from app.models.base import Base


# class Document(Base):
#     __tablename__ = "document"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     profile_id = Column(Integer, ForeignKey("profile.id"), nullable=True)

#     filename = Column(String, nullable=False)
#     path = Column(String, nullable=False)
#     file_type = Column(String, nullable=False)
#     size_kb = Column(Integer, nullable=True)

#     num_pages = Column(Integer, nullable=True)
#     language = Column(String, nullable=True)
#     hash = Column(String, nullable=True)

#     status = Column(String, nullable=False, default="uploaded")
#     error_message = Column(Text, nullable=True)

#     upload_time = Column(TIMESTAMP, server_default=func.current_timestamp())
#     last_processed = Column(TIMESTAMP, nullable=True)

#     # existing relationship
#     profile = relationship("Profile")

#     # ADD THIS relationship for QA with cascade delete
#     qa_entries = relationship(
#         "QA",
#         back_populates="document",
#         cascade="all, delete-orphan"
#     )



from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func, Text
from sqlalchemy.orm import relationship
# Ensure this matches your file path: document_backend/app/models/base.py
from app.models.base import Base 

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
    error_message = Column(Text, nullable=True)

    # --- CRITICAL FIX: Added content_summary for the AI results ---
    content_summary = Column(Text, nullable=True)

    upload_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    last_processed = Column(TIMESTAMP, nullable=True)

    # Existing relationships
    profile = relationship("Profile")

    # QA relationship with cascade delete
    qa_entries = relationship(
        "QA",
        back_populates="document",
        cascade="all, delete-orphan"
    )