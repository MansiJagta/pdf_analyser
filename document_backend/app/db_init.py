# app/db_init.py

from app.database import engine
from app.models.base import Base

# IMPORTANT: Import ALL models so SQLAlchemy registers tables
from app.models.profile_model import Profile
from app.models.document_model import Document
from app.models.summary_model import Summary
from app.models.qa_model import QA
from app.models.embedding_model import Embedding

def init_db():
    Base.metadata.create_all(bind=engine)
