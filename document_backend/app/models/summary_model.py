from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=False)
    persona = Column(String, nullable=True)        # persona name for persona-based summary
    summary_text = Column(Text, nullable=False)
    model_used = Column(String, nullable=True)    # DistilBART / Mistral
    generated_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    document = relationship("Document", backref="summaries")