from __future__ import annotations

from app.ai.openai_client import get_chat_model
from app.ai.qdrant_store import QdrantStore


class RAGService:
    def __init__(self) -> None:
        self.qdrant = QdrantStore()
        self.llm = get_chat_model()

    def answer(self, company_id: int, question: str, conversation_summary: str = "") -> dict:
        chunks = self.qdrant.search(company_id=company_id, query=question, limit=5)
        context = "\n\n".join(f"Source {index + 1}: {chunk.text}" for index, chunk in enumerate(chunks))
        prompt = (
            "You are a helpful enterprise AI assistant. Use the context to answer accurately. "
            "If the answer is not in the context, say what is missing. Cite the sources by number.\n\n"
            f"Conversation summary:\n{conversation_summary}\n\n"
            f"Context:\n{context}\n\nQuestion: {question}"
        )
        response = self.llm.invoke(prompt)
        citations = [
            {
                "source": chunk.metadata.get("filename"),
                "document_id": chunk.metadata.get("document_id"),
                "score": chunk.score,
            }
            for chunk in chunks
        ]
        return {"answer": response.content, "citations": citations}