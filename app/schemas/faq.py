from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FAQCreate(BaseModel):
    """What the user sends when adding a new FAQ."""
    question: str = Field(..., min_length=5)
    answer:  str = Field(..., min_length=5)
    category: Optional[str] = None


class FAQResponse(BaseModel):
    """What we send back to the user."""
    id: int
    question: str
    answer: str
    category: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class AskRequest(BaseModel):
    """What the user sends when asking a question."""
    query: str = Field(..., min_length=3)


class SearchResult(BaseModel):
    """A single FAQ result with its similarity score."""
    faq: FAQResponse
    similarity: float


class AskResponse(BaseModel):
    """The full response when a user asks a question."""
    query: str
    results: list[SearchResult]
    message: str