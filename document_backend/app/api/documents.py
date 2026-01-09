from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_documents():
    """
    List all uploaded documents (later from DB)
    """
    return {"documents": []}
