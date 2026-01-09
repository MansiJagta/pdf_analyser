from sqlalchemy import Column, Integer, String, ForeignKey, BLOB
from sqlalchemy.orm import relationship
from app.models.document_model import Base

class Embedding(Base):
    __tablename__ = "embedding"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=False)
    chunk_text = Column(String, nullable=False)   # chunk of the document
    vector = Column(BLOB, nullable=False)         # embedding vector stored as bytes

    document = relationship("Document", backref="embeddings")
