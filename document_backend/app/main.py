from fastapi import FastAPI
from app.api import documents
from app.db_init import init_db
from app.db.session import engine
from app.models.base import Base
import app.models.document_model 
import app.models.qa_model
import app.models.profile_model

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Offline AI PDF Analyser",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(
    documents.router,
    prefix="/documents",
    tags=["Documents"]
)

@app.get("/")
def health_check():
    return {"status": "ok"}
