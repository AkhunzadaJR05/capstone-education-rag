# Multimodal RAG Platform — Education

A RAG-based platform where students and instructors upload course
material (lecture slides, past papers, audio recordings, etc.) and
ask questions answered directly from those documents.

## Tech Stack
FastAPI · SQLAlchemy + Alembic · SQLite · Qdrant · Streamlit ·
Groq (Llama 3.3) · sentence-transformers

## Status
Day 2 of 5 — Authentication and room management complete.
Ingestion pipeline, RAG chat, and full frontend in progress.

## Setup
\`\`\`bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
\`\`\`

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.