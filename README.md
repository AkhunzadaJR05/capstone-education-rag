# Multimodal RAG Platform — Education

A multimodal RAG (Retrieval-Augmented Generation) platform built for
the Education industry. Students and instructors upload course
material — lecture slides, past papers, assignment briefs, images,
audio and video recordings, spreadsheets — and ask natural-language
questions, receiving answers grounded directly in their own uploaded
content, with sources cited for every response.

## Problem

Course material is scattered across many formats with no unified way
to search across it. Students waste time manually hunting through
slides, past papers, and recordings before exams. Instructors have no
easy way to query their own archive of teaching material. This
platform solves that by letting users upload files once and ask
questions directly, with every answer traceable back to its exact
source file and chunk.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic, SQLite
- Vector store: Qdrant
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- LLM: Groq (Llama 3.3 70B)
- Frontend: Streamlit
- File processing: pymupdf4llm, python-docx, python-pptx, pandas, Tesseract OCR, OpenAI Whisper, ffmpeg

## Supported File Types

PDF, DOCX, CSV, Markdown, TXT, PPTX, Images (PNG/JPG), Audio (MP3/WAV/M4A), Video (MP4/MOV)

## Environment Variables

Create a .env file in the project root with the following:

SECRET_KEY=your-random-secret-key
DATABASE_URL=sqlite:///./app.db
GROQ_API_KEY=your-groq-api-key

SECRET_KEY can be any random string used to sign JWTs. GROQ_API_KEY is required for chat responses to work, get a free key at console.groq.com. Never commit your real .env file; it is already excluded via .gitignore.

## Prerequisites

Besides the Python packages in requirements.txt, two external programs must be installed separately and available on your system PATH:

- Tesseract OCR, required for image text extraction
- ffmpeg, required for audio and video transcription

## Setup

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head

## Running the App

Two terminals are required, running simultaneously.

Terminal 1, backend:
uvicorn main:app --reload

Terminal 2, frontend:
streamlit run streamlit_app.py

The backend runs at http://127.0.0.1:8000 with interactive API docs at /docs. The frontend runs at http://localhost:8501.

## Quick Demo

1. Open http://localhost:8501 and register a new account
2. Log in and create a new chat room
3. Upload a file from the /demo folder, one sample file per supported type is included there
4. Wait for the file to show status ready in the sidebar
5. Ask a question about the uploaded content, the answer will include a Sources section showing exactly which file and chunk it came from
6. Ask a question unrelated to any uploaded content, the system will correctly respond I don't know with no sources, rather than guessing

## Project Structure

main.py, FastAPI app entry point
streamlit_app.py, Streamlit frontend
routers/, API route handlers for auth, rooms, upload, chat
db/, SQLAlchemy models and database setup
services/, Auth, embeddings, RAG logic, vector store
services/ingestion/, Per-file-type extractors
alembic/, Database migrations
demo/, Sample files, one per supported type
docs/architecture.png, Approved system architecture diagram

## Architecture

See docs/architecture.png for the full system architecture diagram, and the accompanying technical document for a detailed component-by-component explanation.
