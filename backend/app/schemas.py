from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationCreate(BaseModel):
    title: str | None = None


class MessageCreate(BaseModel):
    content: str
    image_path: str | None = None
    metadata: str | None = None


class MessageRead(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    image_path: str | None = None
    metadata: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationRead(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DocumentUpload(BaseModel):
    filename: str
    file_type: str
    storage_path: str
    summary: str | None = None


class SourceResponse(BaseModel):
    id: int
    source_type: str
    title: str | None = None
    url: str | None = None
    snippet: str | None = None
