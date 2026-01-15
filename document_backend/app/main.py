# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.api import documents

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
