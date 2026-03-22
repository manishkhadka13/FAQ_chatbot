from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.faq import FAQ, QueryLog
from app.schemas.faq import FAQCreate, SearchResult, FAQResponse
from app.services.embedding import embed
from app.core.config import settings

async def create_faq(db: AsyncSession, data: FAQCreate) -> FAQ:
    """Save a new FAQ and generate its embedding."""
    vector = embed(data.question)  
    faq = FAQ(
        question=data.question,
        answer=data.answer,
        category=data.category,
        embedding=vector,           
    )
    db.add(faq)
    await db.commit()
    await db.refresh(faq)
    return faq

async def list_faqs(db: AsyncSession) -> list[FAQ]:
    """Return all FAQs from the database."""
    result = await db.execute(select(FAQ).order_by(FAQ.created_at.desc()))
    return result.scalars().all()

async def semantic_search(db: AsyncSession, query: str) -> list[SearchResult]:
    """Find the most similar FAQs to the user's question."""

    query_vector = embed(query)

    stmt = text("""
        SELECT id, question, answer, category, created_at,
               1 - (embedding <=> CAST(:vec AS vector)) AS similarity
        FROM   faqs
        WHERE  1 - (embedding <=> CAST(:vec AS vector)) >= :threshold
        ORDER  BY similarity DESC
        LIMIT  :top_k
    """)

    rows = await db.execute(stmt, {
        "vec": str(query_vector),
        "threshold": settings.SIMILARITY_THRESHOLD,
        "top_k": settings.TOP_K_RESULTS,
    })
    rows = rows.mappings().all()

   
    results = []
    for row in rows:
        faq_resp = FAQResponse(
            id=row["id"],
            question=row["question"],
            answer=row["answer"],
            category=row["category"],
            created_at=row["created_at"],
        )
        results.append(SearchResult(faq=faq_resp, similarity=round(row["similarity"], 4)))

   
    log = QueryLog(
        user_query=query,
        matched_faq_id=results[0].faq.id if results else None,
        similarity=results[0].similarity if results else None,
    )
    db.add(log)
    await db.commit()

    return results