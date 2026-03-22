from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.faq import FAQCreate, FAQResponse, AskRequest, AskResponse
from app.services import faq_service

router = APIRouter(prefix="/faq", tags=["FAQ"])

@router.post("/", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
async def add_faq(payload: FAQCreate, db: AsyncSession = Depends(get_db)):
    """Add a new FAQ. Embedding is generated automatically."""
    return await faq_service.create_faq(db, payload)

@router.get("/", response_model=list[FAQResponse])
async def list_faqs(db: AsyncSession = Depends(get_db)):
    """Return all stored FAQs."""
    return await faq_service.list_faqs(db)

@router.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest, db: AsyncSession = Depends(get_db)):
    """Ask a question — returns semantically similar FAQs."""
    results = await faq_service.semantic_search(db, payload.query)
    message = (
        "Here are the most relevant answers I found."
        if results
        else "Sorry, I couldn't find a relevant answer. Try rephrasing your question."
    )
    return AskResponse(query=payload.query, results=results, message=message)

