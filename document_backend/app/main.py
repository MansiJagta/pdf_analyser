# # app/main.py
# from fastapi import FastAPI
# from app.database import engine, Base
# from app.api import documents

# app = FastAPI()

# # Create tables
# Base.metadata.create_all(bind=engine)

# # Register routes
# app.include_router(documents.router, prefix="/documents", tags=["Documents"])









from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import documents

app = FastAPI(title="Offline AI PDF Analyzer API")

# 1. Configure CORS
# This allows your React frontend (usually on port 5173 or 3000) 
# to talk to this backend.
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 2. Create database tables
Base.metadata.create_all(bind=engine)

# 3. Simple Root Route
# This prevents the 404 error when you visit the base URL
@app.get("/")
async def root():
    return {
        "message": "Offline AI PDF Analyzer Backend is Running",
        "docs": "/docs"
    }

# 4. Register routes
app.include_router(documents.router, prefix="/documents", tags=["Documents"])