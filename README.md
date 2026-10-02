# Nexa Mind

Nexa Mind is an AI-powered vision-and-retrieval assistant that combines computer vision, multimodal reasoning, retrieval-augmented generation (RAG), and conversational memory to answer questions grounded in the user’s visual context and retrieved sources.

## What this project includes

- FastAPI backend with authentication, chat, image analysis, and document ingestion
- SQLite database for a lightweight prototype
- Embedding and retrieval pipeline for user-uploaded knowledge
- Vision and object-understanding service with confidence-aware answer generation
- Web retrieval using DuckDuckGo for external context
- Memory layer for short-term conversational grounding
- Modern Next.js frontend with camera-style workflow and chat panel

## Architecture

```text
Frontend (Next.js)
  ↓
Backend API (FastAPI)
  ↓
Authentication and sessions
  ↓
AI Orchestrator
  ├── Vision module
  ├── OCR/text extraction
  ├── Embeddings
  ├── RAG engine
  ├── Web search module
  ├── Memory service
  └── Tool integration
  ↓
LLM reasoning
  ↓
Grounded response + sources
```

## Quick start

### 1. Create a virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```

### 2. Run the backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the app

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

## Environment variables

Use `.env.example` as the starting point and copy it to `.env`.

## Key API routes

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/chat/message`
- `POST /api/images/analyze`
- `POST /api/documents/upload`
- `GET /api/documents`

## Security notes

- Store tokens server-side and never expose API keys in frontend code.
- Use strong secrets in `.env`.
- Sanitize user uploads and validate file types.

## Future upgrades

- Replace mock vision heuristics with multimodal API or local vision model
- Use PostgreSQL with pgvector for production
- Add persistent vector indexes and background indexing jobs
- Add streaming chat UI and tool execution traces
