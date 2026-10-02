from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.memory.memory_service import MemoryService
from app.ai.rag.rag_service import RAGService
from app.ai.orchestration.orchestrator import AIOrchestrator
from app.auth import get_current_user
from app.crud import add_message, create_conversation, get_conversation_by_id, get_conversations_for_user, get_messages_for_conversation, add_source_record
from app.database import get_db_session
from app.models import Conversation, User
from app.schemas import ConversationCreate, ConversationRead, MessageCreate, MessageRead

router = APIRouter()

rag_service = RAGService()
memory_service = MemoryService()
orchestrator = AIOrchestrator(rag_service, memory_service)


@router.get("/conversations", response_model=list[ConversationRead])
def list_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    return get_conversations_for_user(db, current_user.id)


@router.post("/conversations", response_model=ConversationRead)
def create_conversation_endpoint(payload: ConversationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    return create_conversation(db, current_user.id, payload.title)


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageRead])
def get_messages(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    conversation = get_conversation_by_id(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return get_messages_for_conversation(db, conversation_id)


@router.post("/message")
def send_message(
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    conversation = get_conversation_by_id(db, 1, current_user.id)
    if conversation is None:
        conversation = create_conversation(db, current_user.id, "Auto-generated conversation")

    history = [
        {"role": msg.role, "content": msg.content}
        for msg in get_messages_for_conversation(db, conversation.id)
    ]

    results = orchestrator.handle_message(payload.content, payload.image_path, history)

    assistant_answer = results["answer"]
    add_message(db, conversation.id, "user", payload.content, payload.image_path)
    add_message(db, conversation.id, "assistant", assistant_answer)

    if results.get("retrieved"):
        for item in results["retrieved"][:3]:
            add_source_record(
                db,
                conversation.id,
                source_type=results["type"],
                title=item.get("title", "Source"),
                url=item.get("url"),
                snippet=item.get("snippet", ""),
            )

    return {"conversation_id": conversation.id, "response": assistant_answer, "type": results["type"]}
