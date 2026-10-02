from __future__ import annotations

import os
from pathlib import Path
from typing import BinaryIO

from fastapi import UploadFile

from app.config import DOCS_DIR, UPLOAD_DIR


def save_upload_file(file: UploadFile, subfolder: str = "uploads") -> str:
    target_dir = UPLOAD_DIR if subfolder == "uploads" else DOCS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(file.filename).name
    target_path = target_dir / filename

    idx = 1
    while target_path.exists():
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        target_path = target_dir / f"{stem}_{idx}{suffix}"
        idx += 1

    with open(target_path, "wb") as out_file:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            out_file.write(chunk)
    return str(target_path)


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
