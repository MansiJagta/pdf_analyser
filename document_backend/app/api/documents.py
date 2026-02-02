# # from fastapi import APIRouter, UploadFile, File, HTTPException
# # from app.database import get_db
# # from app.models.document_model import Document
# # from sqlalchemy.orm import Session
# # import hashlib
# # import os

# # router = APIRouter()

# # UPLOAD_DIR = "storage/documents/"

# # @router.post("/upload")
# # async def upload_document(file: UploadFile = File(...), db: Session = get_db()):
# #     # 1. Validate file type
# #     if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
# #         raise HTTPException(status_code=400, detail="File type not allowed")

# #     # 2. Read file bytes
# #     file_bytes = await file.read()

# #     # 3. Generate hash
# #     file_hash = hashlib.sha256(file_bytes).hexdigest()

# #     # 4. Check duplicates
# #     existing_doc = db.query(Document).filter(Document.file_hash == file_hash).first()
# #     if existing_doc:
# #         return {"message": "File already exists", "document_id": existing_doc.id}

# #     # 5. Save file
# #     file_path = os.path.join(UPLOAD_DIR, file.filename)
# #     with open(file_path, "wb") as f:
# #         f.write(file_bytes)

# #     # 6. Insert into DB
# #     new_doc = Document(
# #         filename=file.filename,
# #         path=file_path,
# #         file_hash=file_hash
# #     )
# #     db.add(new_doc)
# #     db.commit()
# #     db.refresh(new_doc)

# #     return {
# #         "message": "File uploaded successfully",
# #         "document_id": new_doc.id,
# #         "filename": new_doc.filename
# #     }
# # app/api/documents.py
# import os
# import shutil
# from fastapi import APIRouter, UploadFile, File, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import desc
# from fastapi import HTTPException
# from app.models.qa_model import QA 

# from app.database import get_db
# from app.models.document_model import Document
# from app.utils.local_user import get_or_create_local_user

# # Router
# router = APIRouter(prefix="/documents", tags=["Documents"])

# # Storage directory
# STORAGE_DIR = os.path.join("app", "storage", "documents")
# os.makedirs(STORAGE_DIR, exist_ok=True)


# # ==============================
# # Upload Multiple Documents
# # ==============================
# @router.post("/upload")
# def upload_documents(
#     files: list[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     local_user = get_or_create_local_user(db)
#     uploaded = []

#     for file in files:
#         file_path = os.path.join(STORAGE_DIR, file.filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         size_kb = os.path.getsize(file_path) // 1024
#         file_type = file.filename.split(".")[-1].lower()

#         doc = Document(
#             filename=file.filename,
#             path=file_path,
#             file_type=file_type,
#             size_kb=size_kb,
#             status="uploaded",
#             profile_id=local_user.id
#         )
#         db.add(doc)
#         db.commit()
#         db.refresh(doc)

#         uploaded.append({
#             "id": doc.id,
#             "filename": doc.filename,
#             "size_kb": size_kb,
#             "file_type": file_type
#         })

#     return {
#         "message": "Files uploaded successfully",
#         "user": local_user.username,
#         "count": len(uploaded),
#         "documents": uploaded
#     }


# # ==============================
# # List Documents
# # ==============================
# @router.get("/")
# def list_documents(db: Session = Depends(get_db)):
#     docs = db.query(Document).order_by(desc(Document.upload_time)).all()

#     result = []
#     for d in docs:
#         result.append({
#             "id": d.id,
#             "filename": d.filename,
#             "status": d.status,
#             "upload_time": str(d.upload_time),
#             "file_type": d.file_type,
#             "size_kb": d.size_kb,
#         })

#     return {
#         "count": len(result),
#         "documents": result
#     }
# @router.delete("/{doc_id}")
# def delete_document(doc_id: int, db: Session = Depends(get_db)):
#     doc = db.query(Document).filter(Document.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     # Delete file
#     if os.path.exists(doc.path):
#         os.remove(doc.path)

#     # Delete DB record
#     db.delete(doc)
#     db.commit()

#     return {
#         "message": "Document deleted",
#         "document_id": doc_id
#     }
# @router.get("/{doc_id}")
# def get_document(doc_id: int, db: Session = Depends(get_db)):
#     doc = db.query(Document).filter(Document.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     return {
#         "id": doc.id,
#         "filename": doc.filename,
#         "file_type": doc.file_type,
#         "size_kb": doc.size_kb,
#         "status": doc.status,
#         "upload_time": str(doc.upload_time),
#         "summary": None,          # future
#         "extracted_text": None,   # future
#         "qa_history": []          # future
#     }
# @router.post("/{doc_id}/ask")
# def ask_question(doc_id: int, question: str, db: Session = Depends(get_db)):
#     # 1. Check if document exists
#     doc = db.query(Document).filter(Document.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     # 2. Dummy answer (replace with AI later)
#     answer = "This is a placeholder answer. AI not implemented yet."

#     # 3. Create QA entry
#     qa_entry = QA(
#         document_id=doc.id,
#         question=question,
#         answer=answer
#     )
#     db.add(qa_entry)
#     db.commit()
#     db.refresh(qa_entry)

#     return {
#         "id": qa_entry.id,
#         "document_id": qa_entry.document_id,
#         "question": qa_entry.question,
#         "answer": qa_entry.answer,
#         "asked_at": str(qa_entry.asked_at)
#     }
# @router.get("/{doc_id}/history")
# def get_qa_history(doc_id: int, db: Session = Depends(get_db)):
#     doc = db.query(Document).filter(Document.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     history = db.query(QA).filter(QA.document_id == doc.id).order_by(QA.asked_at).all()

#     result = []
#     for entry in history:
#         result.append({
#             "id": entry.id,
#             "question": entry.question,
#             "answer": entry.answer,
#             "context": entry.context,
#             "model_used": entry.model_used,
#             "asked_at": str(entry.asked_at)
#         })

#     return {
#         "count": len(result),
#         "history": result
#     }

# @router.post("/{document_id}/process")
# def process_doc(
#     document_id: int,
#     db: Session = Depends(get_db)
# ):
#     process_document(document_id, db)
#     return {"message": "Processing started"}

# app/api/documents.py

import os
import shutil
import hashlib
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from pydantic import BaseModel
from fastapi import BackgroundTasks
from app.database import get_db
from app.models.document_model import Document
from app.models.qa_model import QA
from app.utils.local_user import get_or_create_local_user
from app.services.document_processor import process_document  # <-- processor hook
from app.ai.llm import engine
from app.db.session import get_db
router = APIRouter(prefix="/documents", tags=["Documents"])
\

# Storage directory
STORAGE_DIR = os.path.join("app", "storage", "documents")
os.makedirs(STORAGE_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


# ==============================
# Upload Multiple Documents
# ==============================
@router.post("/upload")
async def upload_documents(
    background_tasks: BackgroundTasks, # Added for async AI processing
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    local_user = get_or_create_local_user(db)
    uploaded = []

    for file in files:
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue

        file_bytes = await file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        
        existing = db.query(Document).filter(Document.hash == file_hash).first()
        if existing:
            uploaded.append({"id": existing.id, "filename": existing.filename, "status": existing.status, "duplicate": True})
            continue

        safe_name = f"{file_hash[:10]}_{file.filename}"
        file_path = os.path.join(STORAGE_DIR, safe_name)

        with open(file_path, "wb") as buffer:
            buffer.write(file_bytes)

        doc = Document(
            filename=file.filename,
            path=file_path,
            file_type=ext,
            size_kb=len(file_bytes) // 1024,
            hash=file_hash,
            status="processing", # Set to processing immediately
            profile_id=local_user.id
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # TRIGGER AI IN BACKGROUND
        # This fixes the "No summary available" issue by starting analysis immediately
        background_tasks.add_task(process_document, doc.id)

        uploaded.append({"id": doc.id, "filename": doc.filename, "status": "processing"})

    return {
    "message": "Upload completed",
    "user": local_user.username,
    "count": len(uploaded),
    "documents": uploaded
}

# ==============================
# Ask Question (AI Logic)
# ==============================
# 1. Define the model FIRST
class QuestionRequest(BaseModel):
    question: str

# @router.post("/{doc_id}/ask")
# async def ask_question(doc_id: int, payload: QuestionRequest, db: Session = Depends(get_db)):
#     doc = db.query(Document).filter(Document.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     if doc.status != "processed":
#         raise HTTPException(status_code=400, detail="Document is still being analyzed. Please wait.")

#     context = doc.content_summary if doc.content_summary else "No summary available."
    
#     system_prompt = (
#         "You are an offline AI assistant. Use the following context to answer the user accurately. "
#         "If the answer isn't in the context, say you don't know.\n\n"
#         f"Context: {context}"
#     )

#     try:
#         # Prompt optimization: removing duplicate leading tags for Llama-3.2
#         answer = engine.generate(user_query=payload.question, system_prompt=system_prompt)
#     except Exception as e:
#         answer = f"AI Error: {str(e)}"

#     qa = QA(document_id=doc.id, question=payload.question, answer=answer, asked_at=datetime.utcnow())
#     db.add(qa)
#     db.commit()
#     db.refresh(qa)

#     return {"id": qa.id, "answer": qa.answer, "asked_at": str(qa.asked_at)}

# # ==============================
# # QA History (New Necessity)
# # ==============================
# @router.get("/{doc_id}/history")
# async def get_qa_history(doc_id: int, db: Session = Depends(get_db)):
#     """Allows the frontend to reload previous chat messages for this PDF."""
#     history = db.query(QA).filter(QA.document_id == doc_id).order_by(desc(QA.asked_at)).all()
#     return {
#         "document_id": doc_id,
#         "history": [{"id": q.id, "question": q.question, "answer": q.answer, "at": str(q.asked_at)} for q in history]
#     }

# # ==============================
# # List Documents
# # ==============================
# @router.get("/")
# def list_documents(db: Session = Depends(get_db)):
#     docs = db.query(Document).order_by(desc(Document.upload_time)).all()

#     return {
#         "count": len(docs),
#         "documents": [
#             {
#                 "id": d.id,
#                 "filename": d.filename,
#                 "status": d.status,
#                 "file_type": d.file_type,
#                 "size_kb": d.size_kb,
#                 "upload_time": str(d.upload_time)
#             }
#             for d in docs
#         ]
#     }


# # ==============================
# # Get Single Document
# # ==============================
# @router.get("/{doc_id}")
# def get_document(doc_id: int, db: Session = Depends(get_db)):
#     doc = db.query(Document).filter(Document.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     return {
#         "id": doc.id,
#         "filename": doc.filename,
#         "file_type": doc.file_type,
#         "size_kb": doc.size_kb,
#         "status": doc.status,
#         "upload_time": str(doc.upload_time)
#     }


@router.post("/{doc_id}/ask")
async def ask_question(doc_id: int, payload: QuestionRequest, db: Session = Depends(get_db)):
    # 1. Fetch the document
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2. Check status and return a helpful "Not Ready" response
    if doc.status == "uploaded" or doc.status == "processing":
        return {
            "id": None,
            "status": doc.status,
            "answer": "I am still reading and summarizing your PDF. Please wait a moment.",
            "is_ready": False,
            "progress_tip": "Check back in 30-60 seconds."
        }
    
    if doc.status == "failed":
        return {
            "id": None,
            "status": "failed",
            "answer": "I encountered an error while processing this document. Try re-uploading.",
            "is_ready": False
        }

    # 3. If "processed", proceed to AI Generation
    context = doc.content_summary if doc.content_summary else "Context not available."
    
    system_prompt = (
        "You are a helpful AI assistant. Use the following document context "
        "to answer the user's question.\n\n"
        f"Context: {context}"
    )

    try:
        answer = engine.generate(user_query=payload.question, system_prompt=system_prompt)
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        answer = "I'm sorry, I had trouble generating an answer right now."

    # 4. Save to History
    qa = QA(
        document_id=doc.id,
        question=payload.question,
        answer=answer,
        asked_at=datetime.utcnow()
    )
    db.add(qa)
    db.commit()
    db.refresh(qa)

    return {
        "id": qa.id,
        "status": "processed",
        "is_ready": True,
        "question": qa.question,
        "answer": qa.answer,
        "asked_at": str(qa.asked_at)
    }
# ==============================
# Process Document (AI Hook)
# ==============================
@router.post("/{doc_id}/process")
def process_doc(doc_id: int, db: Session = Depends(get_db)):
    process_document(doc_id, db)
    return {"message": "Processing started"}

@router.get("/{doc_id}/summary")
async def get_document_summary(doc_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the AI-generated summary for a specific document.
    """
    # 1. Fetch the document by ID
    doc = db.query(Document).filter(Document.id == doc_id).first()
    
    # 2. Check if document exists
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 3. Check if the summary is actually there
    if not doc.content_summary:
        # If status is still 'processing', tell the user to wait
        if doc.status == "processing":
            return {
                "document_id": doc_id,
                "status": "processing",
                "message": "AI is still analyzing the PDF. Please try again in a moment."
            }
        return {
            "document_id": doc_id,
            "status": doc.status,
            "message": "No summary available for this document."
        }

    # 4. Return the summary
    return {
        "document_id": doc_id,
        "filename": doc.filename,
        "summary": doc.content_summary,
        "status": doc.status
    }