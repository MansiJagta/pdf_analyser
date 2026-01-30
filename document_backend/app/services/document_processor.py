# app/services/document_processor.py

from sqlalchemy.orm import Session
from app.models.document_model import Document
from datetime import datetime

def process_document(document_id: int, db: Session):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise ValueError("Document not found")

    try:
        # 1. mark processing
        document.status = "processing"
        db.commit()

        # 2. (AI PIPELINE WILL COME HERE)
        # layout_detection()
        # text_extraction()
        # summarization()
        # embeddings()

        # 3. mark processed
        document.status = "processed"
        document.last_processed = datetime.utcnow()
        db.commit()

    except Exception as e:
        document.status = "failed"
        document.error_message = str(e)
        db.commit()
        raise
# # app/services/document_processor.py

# from sqlalchemy.orm import Session
# from app.models.document_model import Document
# from datetime import datetime

# def process_document(document_id: int, db: Session):
#     document = db.query(Document).filter(Document.id == document_id).first()

#     if not document:
#         raise ValueError("Document not found")

#     try:
#         document.status = "processing"
#         db.commit()

#         # AI PIPELINE (later)
#         # layout_detection()
#         # text_extraction()
#         # summarization()
#         # embeddings()

#         document.status = "processed"
#         document.last_processed = datetime.utcnow()
#         db.commit()

#     except Exception as e:
#         document.status = "failed"
#         db.commit()
#         raise
# from sqlalchemy.orm import Session
# from app.models.document_model import Document
# from app.services.ai_service import run_document_ai
# from datetime import datetime

# def process_document(document_id: int, db: Session):
#     document = db.query(Document).filter(Document.id == document_id).first()

#     if not document:
#         raise ValueError("Document not found")

#     try:
#         document.status = "processing"
#         db.commit()

#         # 🔥 AI INTEGRATION (STEP 1 COMPLETE HERE)
#         ai_result = run_document_ai(
#             file_path=document.path,
#             persona=document.profile_id  # or profile.persona
#         )

#         # TEMP: just log / print
#         print("📄 AI SUMMARY:", ai_result["summary"][:200])

#         document.status = "processed"
#         document.last_processed = datetime.utcnow()
#         db.commit()

#     except Exception as e:
#         document.status = "failed"
#         document.error_message = str(e)
#         db.commit()
#         raise
