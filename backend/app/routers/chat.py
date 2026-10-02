from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db_session
from app.crud import create_user, get_user_by_email
from app.models import User
from app.schemas import TokenResponse, UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register_user(payload: UserCreate, db: Session = Depends(get_db_session)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = create_user(db, payload.email, hash_password(payload.password))
    return user


@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserCreate, db: Session = Depends(get_db_session)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenResponse(access_token=create_access_token(user.email), token_type="bearer")
