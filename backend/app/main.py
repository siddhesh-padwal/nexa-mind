from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import BACKEND_CORS_ORIGINS
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.documents import router as documents_router
from app.routers.images import router as images_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nexa Mind",
    description="AI-powered vision-and-retrieval assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "nexa-mind"}


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(images_router, prefix="/api/images", tags=["images"])
app.include_router(documents_router, prefix="/api/documents", tags=["documents"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
