import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models
from app.models.profile_model import Base as ProfileBase
from app.models.document_model import Base as DocumentBase
from app.models.summary_model import Base as SummaryBase
from app.models.qa_model import Base as QABase
from app.models.embedding_model import Base as EmbeddingBase

# Create all tables
ProfileBase.metadata.create_all(bind=engine)
DocumentBase.metadata.create_all(bind=engine)
SummaryBase.metadata.create_all(bind=engine)
QABase.metadata.create_all(bind=engine)
EmbeddingBase.metadata.create_all(bind=engine)
