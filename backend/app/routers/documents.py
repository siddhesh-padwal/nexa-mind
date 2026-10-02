from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.ai.vision.vision_service import analyze_image
from app.auth import get_current_user
from app.database import get_db_session
from app.models import User
from app.utils import save_upload_file

router = APIRouter()


@router.post("/analyze")
def analyze_uploaded_image(
    prompt: str = Form(default=""),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A file is required")

    saved_path = save_upload_file(file)
    result = analyze_image(saved_path, prompt)
    return {"file_path": saved_path, "analysis": result}
