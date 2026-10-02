from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
DOCS_DIR = DATA_DIR / "docs"

for directory in [DATA_DIR, UPLOAD_DIR, DOCS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/app/nexa_mind.db")
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(",")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
