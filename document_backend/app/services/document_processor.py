import os
import logging
from sqlalchemy.orm import Session
from app.models.base import Document
from app.ai.manager import app as ai_app  # This is your LangGraph instance

# Set up logging to track the processing steps in your terminal
logger = logging.getLogger(__name__)

async def process_document(db: Session, document_id: int):
    """
    Main background task to process a PDF using the LangGraph AI pipeline.
    """
    # 1. Fetch document from SQLite
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        logger.error(f"Document {document_id} not found in database.")
        return

    try:
        # 2. Update status to 'processing'
        doc.status = "processing"
        db.commit()
        logger.info(f"--- Starting AI Pipeline for: {doc.filename} ---")

        # 3. Prepare the initial state for the LangGraph
        # We pass the physical path to the PDF on your disk
        initial_state = {
            "file_path": doc.file_path,
            "document_id": str(doc.id),
            "metadata": {"filename": doc.filename},
            "content": "",
            "summary": ""
        }

        # 4. Execute the Graph
        # This triggers the Layout Detection -> Text Extraction -> Indexing flow
        # defined in your manager.py and nodes.py
        result = await ai_app.ainvoke(
            initial_state, 
            config={"configurable": {"thread_id": str(doc.id)}}
        )

        # 5. Update the document with AI results
        doc.content_summary = result.get("summary", "No summary generated.")
        doc.status = "processed"
        logger.info(f"✅ Successfully processed: {doc.filename}")

    except Exception as e:
        # 6. Handle failures (e.g., RAM limit hit or file corrupted)
        logger.error(f"❌ Processing failed for {doc.filename}: {str(e)}")
        doc.status = "failed"
    
    finally:
        db.commit()