# 🤖 FAQ Semantic Search Chatbot

A full-stack AI-powered FAQ chatbot that answers questions using **semantic search** — not keyword matching.

Built with **FastAPI**, **PostgreSQL + pgvector**, and **Streamlit**.

---

## 🧠 How It Works
```
User question
     │
     ▼
sentence-transformers  → converts text into a 384-dimensional vector
     │
     ▼
pgvector cosine search → finds the closest FAQ vectors in PostgreSQL
     │
     ▼
Top matching answers   → returned and displayed in Streamlit
```

Instead of `WHERE question LIKE '%return%'`, we embed the question
into a vector and search for nearest neighbours in high-dimensional space.

This means "how do I get my money back?" correctly matches
"What is your return policy?" even though they share zero words.

---

## 🗂️ Project Structure
```
faq-chatbot/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── api/routes/faq.py        # HTTP endpoints
│   ├── core/config.py           # Reads .env settings
│   ├── db/session.py            # Async database connection
│   ├── models/faq.py            # Database table definitions
│   ├── schemas/faq.py           # Request/response shapes
│   └── services/
│       ├── embedding.py         # Text → vector using sentence-transformers
│       └── faq_service.py       # Business logic
├── scripts/
│   └── generate_embeddings.py  # Generate embeddings for existing FAQs
├── streamlit_app.py             # Client-facing UI
├── docker-compose.yml           # PostgreSQL + pgvector container
├── requirements.txt
└── .env.example
```

---

## ⚡ Quick Start

### 1 — Prerequisites
- Python 3.11+
- Docker Desktop

### 2 — Clone the repo
```bash
git clone https://github.com/manishkhadka13/FAQ_chatbot.git
cd FAQ_chatbot
```

### 3 — Create virtual environment
```bash
conda create -n faq_chatbot python=3.11
conda activate faq_chatbot
pip install -r requirements.txt
```

### 4 — Configure environment
```bash
cp .env.example .env
```

### 5 — Start the database
```bash
docker-compose up -d
```

### 6 — Start the API
```bash
uvicorn app.main:app --reload --port 8000
```

### 7 — Start the UI
```bash
streamlit run streamlit_app.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/faq/ask` | Ask a question — returns semantic matches |
| POST | `/faq/` | Add a new FAQ |
| GET | `/faq/` | List all FAQs |
| GET | `/health` | Health check |

Interactive docs available at: `http://localhost:8000/docs`

---


## 📚 Learning Resources

- [pgvector docs](https://github.com/pgvector/pgvector)
- [sentence-transformers docs](https://www.sbert.net/)
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
