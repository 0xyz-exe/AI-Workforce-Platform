from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_user
from app.db.session import SessionLocal
from app.models.entities import User
from app.schemas.chat import ChatSessionCreate, ChatSessionRead, MessageCreate, MessageRead
from app.services.chat import ChatService

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionRead)
def create_chat_session(payload: ChatSessionCreate, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> ChatSessionRead:
    service = ChatService(session)
    chat_session = service.create_session(current_user.company_id, current_user.id, payload.agent_id, payload.knowledge_base_id, payload.title)
    return ChatSessionRead.model_validate(chat_session)


@router.post("/sessions/{chat_session_id}/messages", response_model=MessageRead)
def add_message(chat_session_id: int, payload: MessageCreate, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> MessageRead:
    service = ChatService(session)
    message = service.add_message(current_user.company_id, chat_session_id, "user", payload.content)
    return MessageRead.model_validate(message)


@router.post("/sessions/{chat_session_id}/answer")
def answer(chat_session_id: int, payload: MessageCreate, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> dict:
    service = ChatService(session)
    try:
        service.add_message(current_user.company_id, chat_session_id, "user", payload.content)
        result = service.answer_with_rag(chat_session_id, payload.content)
        service.add_message(current_user.company_id, chat_session_id, "assistant", result["answer"])
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.websocket("/sessions/{chat_session_id}/stream")
async def stream_chat(websocket: WebSocket, chat_session_id: int) -> None:
    await websocket.accept()
    try:
        with SessionLocal() as session:
            service = ChatService(session)
            while True:
                payload = await websocket.receive_json()
                question = payload.get("content", "")
                result = service.answer_with_rag(chat_session_id, question)
                await websocket.send_json(result)
    except WebSocketDisconnect:
        return