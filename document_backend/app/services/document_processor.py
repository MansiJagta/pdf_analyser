import os
import logging
from app.models.document_model import Document
from app.ai.manager import app as ai_app
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

async def process_document(document_id: int): 
    """
    Main background task. Creates its own DB session to stay alive 
    after the API response is sent.
    """
    print(f"--- 🚀 BACKGROUND TASK INITIATED FOR ID: {document_id} ---")
    
    # 1. Create a fresh session for THIS background thread
    db = SessionLocal()
    
    import asyncio
    
    try:
        # 2. Fetch document with RETRY logic
        # Sometimes background tasks start before the DB commit is fully visible in a new session
        doc = None
        for attempt in range(3):
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                break
            print(f"⚠️ Attempt {attempt+1}: Document {document_id} not found... retrying in 1s")
            await asyncio.sleep(1)
            
        if not doc:
            logger.error(f"❌ Document {document_id} not found after retries.")
            # Debug: what DOES exist?
            all_ids = [d.id for d in db.query(Document).all()]
            print(f"DEBUG: Visible Document IDs: {all_ids}")
            print(f"DEBUG: CWD: {os.getcwd()}")
            return
        
        print(f"--- 🔄 UPDATING STATUS TO PROCESSING FOR: {doc.filename}---")

        # 3. Update status to 'processing'
        # doc.status = "processing" # Already set in endpoint, but good to double check
        # db.commit()
        logger.info(f"--- 🔄 Starting AI Pipeline for: {doc.filename} ---")

        # 4. Prepare initial state
        # Ensure correct keys for GraphState in app/ai/state.py
        initial_state = {
            "file_path": doc.path, 
            "persona": "executive", # Default persona
            "raw_text": "",
            "layout_type": "",
            "vector_status": "pending",
            "query": "Summarize this document",
            "draft": "",
            "critique": "",
            "reflection_count": 0,
            "errors": [],
            "summary": ""
        }

        # 5. Execute the Graph
        # Using .ainvoke for async execution
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
        import traceback
        logger.error(f"❌ Processing failed: {str(e)}")
        traceback.print_exc() 
        
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            db.commit()
            
    finally:
        # 7. CRITICAL: Always close the session
        db.close()
