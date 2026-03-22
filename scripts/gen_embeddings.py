import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.faq import FAQ
from app.services.embedding import embed


async def generate_embeddings():
    async with AsyncSessionLocal() as db:
        # Find all FAQs with no embedding
        result = await db.execute(
            select(FAQ).where(FAQ.embedding == None)
        )
        faqs = result.scalars().all()

        print(f"Found {len(faqs)} FAQs with missing embeddings...")

        for i, faq in enumerate(faqs, 1):
            faq.embedding = embed(faq.question)
            print(f"  [{i:02d}/{len(faqs)}] ✓ {faq.question[:60]}")

        await db.commit()
        print("\nDone! All embeddings generated.")


if __name__ == "__main__":
    asyncio.run(generate_embeddings())