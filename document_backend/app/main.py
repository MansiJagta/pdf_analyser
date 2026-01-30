# # app/main.py
# from fastapi import FastAPI
# from app.database import engine, Base
# from app.api import documents

# app = FastAPI()

# # Create tables
# Base.metadata.create_all(bind=engine)

# # Register routes
# app.include_router(documents.router, prefix="/documents", tags=["Documents"])
# app/main.py
from fastapi import FastAPI
from app.api import documents
from app.db_init import init_db

app = FastAPI(
    title="Document AI Analysis System",
    version="0.1.0"
)

# Run once when app starts
@app.on_event("startup")
def on_startup():
    init_db()

# Register routes
app.include_router(
    documents.router,
    prefix="/documents",
    tags=["Documents"]
)

@app.get("/")
def health_check():
    return {"status": "ok"}
