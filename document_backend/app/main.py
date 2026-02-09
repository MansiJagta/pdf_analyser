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

from contextlib import asynccontextmanager
from app.core.engine_manager import start_ollama_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: specific order matters
    print("--- 🚀 BACKEND STARTING UP ---")
    start_ollama_engine() # 1. Ensure AI is running or try to start it
    init_db()             # 2. Ensure DB is ready
    yield
    # Shutdown logic (if any)
    print("--- 🛑 BACKEND SHUTTING DOWN ---")

app = FastAPI(
    title="Offline AI PDF Analyser",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(
    documents.router,
    prefix="/documents",
    tags=["Documents"]
)

@app.get("/")
def health_check():
    return {"status": "ok"}
