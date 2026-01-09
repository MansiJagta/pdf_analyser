from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.models.document_model import Base

class QA(Base):
    __tablename__ = "qa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    context = Column(Text, nullable=True)       # optional, retrieved context
    model_used = Column(String, nullable=True)  # e.g., "E5-base-v2"
    asked_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    document = relationship("Document", backref="qa_entries")
