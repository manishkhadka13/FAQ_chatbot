# FAQ Semantic Search Chatbot

A production-ready REST API that answers user questions using **semantic search** — not keyword matching.  
Built with **FastAPI**, **PostgreSQL + pgvector**, and **sentence-transformers**.

---

## 🧠 How It Works

```
User question
     │
     ▼
sentence-transformers          ← converts text → 384-dim vector
     │
     ▼
pgvector cosine similarity     ← finds closest FAQ vectors in Postgres
     │
     ▼
Top-K ranked FAQ answers       ← returned as JSON
```

Instead of `WHERE question LIKE '%return%'`, we embed the question into a vector
and search for the nearest neighbours in high-dimensional space.  
This means *"Can I send something back?"* correctly matches *"What is your return policy?"*.

---

## 🗂️ Project Structure

```
faq-chatbot/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   └── routes/
│   │       └── faq.py           # All HTTP endpoints
│   ├── core/
│   │   └── config.py            # Pydantic settings (reads .env)
│   ├── db/
│   │   └── session.py           # Async SQLAlchemy engine + session
│   ├── models/
│   │   └── faq.py               # SQLAlchemy ORM models (FAQ, QueryLog)
│   ├── schemas/
│   │   └── faq.py               # Pydantic request/response schemas
│   └── services/
│       ├── embedding.py         # Loads sentence-transformer, exposes embed()
│       └── faq_service.py       # Business logic (create, list, semantic search)
├── scripts/
│   └── init.sql                 # Runs on first DB start: enables pgvector, creates tables
├── tests/
│   └── test_faq.py              # Integration tests (httpx)
├── .env.example                 # Copy → .env and fill in
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1 — Prerequisites

| Tool | Version |
|------|---------|
| Docker | 24+ |
| Docker Compose | v2 |

### 2 — Clone & configure

```bash
git clone https://github.com/manishkhadka13/FAQ_chatbot.git
cd FAQ_chatbot

cp .env.example .env
# .env is pre-filled with safe defaults — no changes needed for local dev
```

### 3 — Build & run

```bash
docker-compose up --build
```

This will:
1. Pull `pgvector/pgvector:pg16` and start Postgres
2. Run `scripts/init.sql` — enables the `vector` extension and seeds 5 sample FAQs
3. Build the Python image (downloads the embedding model ~90 MB)
4. Start the FastAPI server on **http://localhost:8000**

> ⏱️ First build takes ~3 min. Subsequent starts are instant.

### 4 — Open the interactive docs

```
http://localhost:8000/docs
```

FastAPI auto-generates a full Swagger UI — try every endpoint from your browser.

---

## 📡 API Endpoints

### `POST /faq/ask` — Ask a question
The core endpoint. Embed the query and return the closest FAQ answers.

**Request**
```json
{ "query": "how can I get my money back?" }
```

**Response**
```json
{
  "query": "how can I get my money back?",
  "message": "Here are the most relevant answers I found.",
  "results": [
    {
      "similarity": 0.8312,
      "faq": {
        "id": 1,
        "question": "What is your return policy?",
        "answer": "You can return any item within 30 days of purchase for a full refund.",
        "category": "orders",
        "created_at": "2024-01-01T00:00:00"
      }
    }
  ]
}
```

---

### `POST /faq/` — Add a FAQ (admin)
Add a new FAQ. The embedding is generated server-side automatically.

```json
{
  "question": "Do you have a mobile app?",
  "answer": "Yes! Download it from the App Store or Google Play.",
  "category": "general"
}
```

---

### `GET /faq/` — List all FAQs

Returns all stored FAQ entries.

---

### `GET /health` — Health check

```json
{ "status": "ok" }
```

---

## 🔬 Running Tests

With the stack running (`docker-compose up`):

```bash
pip install httpx pytest
pytest tests/ -v
```

---




## 📚 Learning Resources

- [pgvector docs](https://github.com/pgvector/pgvector)
- [sentence-transformers docs](https://www.sbert.net/)
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
