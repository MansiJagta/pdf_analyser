import os
import logging
from sqlalchemy.orm import Session
from app.models.document_model import Document
from app.ai.manager import app as ai_app  # This is your LangGraph instance
from app.db.session import SessionLocal  # Ensure this import points to your SessionLocal
from app.models.document_model import Document
import logging

logger = logging.getLogger(__name__)

async def process_document(document_id: int): # Remove 'db' from arguments
    """
    Main background task. Creates its own DB session to stay alive 
    after the API response is sent.
    """
    print(f"--- 🚀 BACKGROUND TASK INITIATED FOR ID: {document_id} ---")
    # 1. Create a fresh session for THIS background thread
    db = SessionLocal()
    
    try:
        # 2. Fetch document
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            logger.error(f"Document {document_id} not found.")
            return
        
        print(f"--- 🔄 UPDATING STATUS TO PROCESSING FOR: {doc.filename}---")

        # 3. Update status to 'processing'
        doc.status = "processing"
        db.commit()
        logger.info(f"--- 🔄 Starting AI Pipeline for: {doc.filename} ---")

        # 4. Prepare initial state (Note: Ensure 'path' matches your model field)
        initial_state = {
            "file_path": doc.path, # Updated from doc.file_path to doc.path to match your model
            "document_id": str(doc.id),
            "metadata": {"filename": doc.filename},
            "content": "",
            "summary": ""
        }

        # 5. Execute the Graph
        # This is where your Llama-3.2-3B model starts working
        result = await ai_app.ainvoke(
            initial_state, 
            config={"configurable": {"thread_id": str(doc.id)}}
        )

        # 6. Save results
        doc.content_summary = result.get("summary", "No summary generated.")
        doc.status = "processed"
        db.commit()
        logger.info(f"✅ Successfully processed: {doc.filename}")

    except Exception as e:
        # This will print the EXACT error in your terminal
        import traceback
        logger.error(f"❌ Processing failed: {str(e)}")
        traceback.print_exc() 
        
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "failed"
            db.commit()
            
    finally:
        # 7. CRITICAL: Always close the session in a background task
        db.close()