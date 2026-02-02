
# from fastapi import FastAPI
# from app.api import documents
# from app.db_init import init_db

# app = FastAPI(
#     title="Document AI Analysis System",
#     version="0.1.0"
# )

# # Run once when app starts
# @app.on_event("startup")
# def on_startup():
#     init_db()

# # Register routes
# app.include_router(
#     documents.router,
#     prefix="/documents",
#     tags=["Documents"]
# )

# @app.get("/")
# def health_check():
#     return {"status": "ok"}





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

app = FastAPI(title="Offline AI PDF Analyser")

app.include_router(documents.router)

app = FastAPI(
    title="Document AI Analysis System",
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
