from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.ai.rag.rag_service import RAGService
from app.auth import get_current_user
from app.crud import create_document, get_documents_for_user
from app.database import get_db_session
from app.models import User
from app.utils import save_upload_file

router = APIRouter()
rag_service = RAGService()


def extract_text_from_file(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    if suffix in {".txt", ".md"}:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)

    if suffix == ".docx":
        from docx import Document

        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    return ""


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    saved_path = save_upload_file(file, subfolder="docs")
    file_type = Path(file.filename).suffix.lower().lstrip(".")
    extracted_text = extract_text_from_file(saved_path)

    if not extracted_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to extract text from the uploaded file")

    rag_service.add_document(file.filename, extracted_text, {"user_id": current_user.id})
    create_document(db, current_user.id, file.filename, file_type, saved_path, summary=extracted_text[:300])

    return {"filename": file.filename, "file_type": file_type, "summary": extracted_text[:300]}


@router.get("")
def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    return get_documents_for_user(db, current_user.id)
