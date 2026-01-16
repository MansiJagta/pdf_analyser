# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.database import get_db
# from app.models.document_model import Document
# from sqlalchemy.orm import Session
# import hashlib
# import os

# router = APIRouter()

# UPLOAD_DIR = "storage/documents/"

# @router.post("/upload")
# async def upload_document(file: UploadFile = File(...), db: Session = get_db()):
#     # 1. Validate file type
#     if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
#         raise HTTPException(status_code=400, detail="File type not allowed")

#     # 2. Read file bytes
#     file_bytes = await file.read()

#     # 3. Generate hash
#     file_hash = hashlib.sha256(file_bytes).hexdigest()

#     # 4. Check duplicates
#     existing_doc = db.query(Document).filter(Document.file_hash == file_hash).first()
#     if existing_doc:
#         return {"message": "File already exists", "document_id": existing_doc.id}

#     # 5. Save file
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         f.write(file_bytes)

#     # 6. Insert into DB
#     new_doc = Document(
#         filename=file.filename,
#         path=file_path,
#         file_hash=file_hash
#     )
#     db.add(new_doc)
#     db.commit()
#     db.refresh(new_doc)

#     return {
#         "message": "File uploaded successfully",
#         "document_id": new_doc.id,
#         "filename": new_doc.filename
#     }
# app/api/documents.py
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from app.models.qa_model import QA 

from app.database import get_db
from app.models.document_model import Document
from app.utils.local_user import get_or_create_local_user

# Router
router = APIRouter(prefix="/documents", tags=["Documents"])

# Storage directory
STORAGE_DIR = os.path.join("app", "storage", "documents")
os.makedirs(STORAGE_DIR, exist_ok=True)


# ==============================
# Upload Multiple Documents
# ==============================
@router.post("/upload")
def upload_documents(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    local_user = get_or_create_local_user(db)
    uploaded = []

    for file in files:
        file_path = os.path.join(STORAGE_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        size_kb = os.path.getsize(file_path) // 1024
        file_type = file.filename.split(".")[-1].lower()

        doc = Document(
            filename=file.filename,
            path=file_path,
            file_type=file_type,
            size_kb=size_kb,
            status="uploaded",
            profile_id=local_user.id
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        uploaded.append({
            "id": doc.id,
            "filename": doc.filename,
            "size_kb": size_kb,
            "file_type": file_type
        })

    return {
        "message": "Files uploaded successfully",
        "user": local_user.username,
        "count": len(uploaded),
        "documents": uploaded
    }


# ==============================
# List Documents
# ==============================
@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(desc(Document.upload_time)).all()

    result = []
    for d in docs:
        result.append({
            "id": d.id,
            "filename": d.filename,
            "status": d.status,
            "upload_time": str(d.upload_time),
            "file_type": d.file_type,
            "size_kb": d.size_kb,
        })

    return {
        "count": len(result),
        "documents": result
    }
@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file
    if os.path.exists(doc.path):
        os.remove(doc.path)

    # Delete DB record
    db.delete(doc)
    db.commit()

    return {
        "message": "Document deleted",
        "document_id": doc_id
    }
@router.get("/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "size_kb": doc.size_kb,
        "status": doc.status,
        "upload_time": str(doc.upload_time),
        "summary": None,          # future
        "extracted_text": None,   # future
        "qa_history": []          # future
    }
@router.post("/{doc_id}/ask")
def ask_question(doc_id: int, question: str, db: Session = Depends(get_db)):
    # 1. Check if document exists
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2. Dummy answer (replace with AI later)
    answer = "This is a placeholder answer. AI not implemented yet."

    # 3. Create QA entry
    qa_entry = QA(
        document_id=doc.id,
        question=question,
        answer=answer
    )
    db.add(qa_entry)
    db.commit()
    db.refresh(qa_entry)

    return {
        "id": qa_entry.id,
        "document_id": qa_entry.document_id,
        "question": qa_entry.question,
        "answer": qa_entry.answer,
        "asked_at": str(qa_entry.asked_at)
    }
@router.get("/{doc_id}/history")
def get_qa_history(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    history = db.query(QA).filter(QA.document_id == doc.id).order_by(QA.asked_at).all()

    result = []
    for entry in history:
        result.append({
            "id": entry.id,
            "question": entry.question,
            "answer": entry.answer,
            "context": entry.context,
            "model_used": entry.model_used,
            "asked_at": str(entry.asked_at)
        })

    return {
        "count": len(result),
        "history": result
    }

