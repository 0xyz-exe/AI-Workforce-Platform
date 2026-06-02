from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from app.core.config import get_settings
from app.ai.openai_client import get_embeddings

settings = get_settings()


@dataclass(slots=True)
class ChunkResult:
    text: str
    score: float
    metadata: dict[str, Any]


class QdrantStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        self.collection_name = settings.qdrant_collection
        self.vector_size = 1536

    def ensure_collection(self) -> None:
        existing = {collection.name for collection in self.client.get_collections().collections}
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qm.VectorParams(size=self.vector_size, distance=qm.Distance.COSINE),
            )

    def upsert_chunks(self, company_id: int, document_id: int, chunks: list[str], metadata: dict[str, Any]) -> None:
        self.ensure_collection()
        embeddings = get_embeddings().embed_documents(chunks)
        points = []
        for index, (chunk, vector) in enumerate(zip(chunks, embeddings, strict=True)):
            points.append(
                qm.PointStruct(
                    id=f"{company_id}:{document_id}:{index}",
                    vector=vector,
                    payload={
                        "company_id": company_id,
                        "document_id": document_id,
                        "chunk_index": index,
                        "text": chunk,
                        **metadata,
                    },
                )
            )
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, company_id: int, query: str, limit: int = 5) -> list[ChunkResult]:
        self.ensure_collection()
        query_vector = get_embeddings().embed_query(query)
        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=qm.Filter(
                must=[qm.FieldCondition(key="company_id", match=qm.MatchValue(value=company_id))]
            ),
        )
        results: list[ChunkResult] = []
        for point in response:
            payload = point.payload or {}
            results.append(
                ChunkResult(text=str(payload.get("text", "")), score=float(point.score or 0.0), metadata=dict(payload))
            )
        return results