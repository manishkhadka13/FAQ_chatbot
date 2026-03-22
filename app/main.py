from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import faq

app = FastAPI(
    title="FAQ Semantic Search Chatbot",
    description="Ask questions in natural language and get answers via semantic search.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(faq.router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}

