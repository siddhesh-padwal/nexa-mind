from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models import Conversation, Document, Message, SourceRecord, User


def create_user(db: Session, email: str, password_hash: str) -> User:
    user = User(email=email, hashed_password=password_hash, is_active=True, created_at=datetime.utcnow())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_conversation(db: Session, user_id: int, title: str | None = None) -> Conversation:
    conversation = Conversation(user_id=user_id, title=title or "New conversation", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversations_for_user(db: Session, user_id: int) -> list[Conversation]:
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()


def get_conversation_by_id(db: Session, conversation_id: int, user_id: int | None = None) -> Conversation | None:
    query = db.query(Conversation).filter(Conversation.id == conversation_id)
    if user_id is not None:
        query = query.filter(Conversation.user_id == user_id)
    return query.first()


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
    image_path: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        image_path=image_path,
        metadata=str(metadata) if metadata is not None else None,
        created_at=datetime.utcnow(),
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_for_conversation(db: Session, conversation_id: int) -> list[Message]:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()


def create_document(db: Session, user_id: int, filename: str, file_type: str, storage_path: str, summary: str | None = None) -> Document:
    document = Document(user_id=user_id, filename=filename, file_type=file_type, storage_path=storage_path, summary=summary, created_at=datetime.utcnow())
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_documents_for_user(db: Session, user_id: int) -> list[Document]:
    return db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()


def add_source_record(db: Session, conversation_id: int, source_type: str, title: str | None = None, url: str | None = None, snippet: str | None = None) -> SourceRecord:
    source = SourceRecord(conversation_id=conversation_id, source_type=source_type, title=title, url=url, snippet=snippet, created_at=datetime.utcnow())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def get_sources_for_conversation(db: Session, conversation_id: int) -> list[SourceRecord]:
    return db.query(SourceRecord).filter(SourceRecord.conversation_id == conversation_id).order_by(SourceRecord.created_at.desc()).all()
