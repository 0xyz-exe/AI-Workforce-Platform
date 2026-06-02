from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Agent, ChatSession, Message
from app.services.rag import RAGService


class ChatService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.rag = RAGService()

    def create_session(self, company_id: int, user_id: int, agent_id: int, knowledge_base_id: int | None, title: str) -> ChatSession:
        chat_session = ChatSession(
            company_id=company_id,
            user_id=user_id,
            agent_id=agent_id,
            knowledge_base_id=knowledge_base_id,
            title=title,
        )
        self.session.add(chat_session)
        self.session.commit()
        return chat_session

    def add_message(self, company_id: int, chat_session_id: int, sender_role: str, content: str) -> Message:
        message = Message(
            company_id=company_id,
            chat_session_id=chat_session_id,
            sender_role=sender_role,
            content=content,
        )
        self.session.add(message)
        self.session.commit()
        return message

    def answer_with_rag(self, chat_session_id: int, question: str) -> dict:
        chat_session = self.session.get(ChatSession, chat_session_id)
        if chat_session is None:
            raise ValueError("Chat session not found")
        summary = "\n".join(message.content for message in chat_session.messages[-6:])
        result = self.rag.answer(chat_session.company_id, question, conversation_summary=summary)
        return result