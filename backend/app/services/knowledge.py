from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

import boto3
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.ingestion import DocumentIngestionService
from app.ai.qdrant_store import QdrantStore
from app.core.config import get_settings
from app.models.entities import Document, KnowledgeBase

settings = get_settings()


class KnowledgeService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.ingestion = DocumentIngestionService()
        self.qdrant = QdrantStore()
        self.s3 = boto3.client(
            "s3",
            region_name=settings.aws_region,
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def create_knowledge_base(self, company_id: int, name: str, description: str | None = None, is_default: bool = False) -> KnowledgeBase:
        kb = KnowledgeBase(company_id=company_id, name=name, description=description, is_default=is_default)
        self.session.add(kb)
        self.session.commit()
        return kb

    def upload_document(self, company_id: int, knowledge_base_id: int, uploaded_by_id: int | None, file: UploadFile) -> Document:
        if file.filename is None:
            raise ValueError("Missing filename")

        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.file.read())
            temp_path = temp_file.name

        s3_key = f"companies/{company_id}/knowledge/{knowledge_base_id}/{file.filename}"
        self.s3.upload_file(temp_path, settings.aws_bucket, s3_key, ExtraArgs={"ContentType": file.content_type or "application/octet-stream"})

        document = Document(
            company_id=company_id,
            knowledge_base_id=knowledge_base_id,
            uploaded_by_id=uploaded_by_id,
            filename=file.filename,
            mime_type=file.content_type or "application/octet-stream",
            file_size=Path(temp_path).stat().st_size,
            s3_key=s3_key,
            status="processing",
        )
        self.session.add(document)
        self.session.flush()

        self.process_document(document.id, temp_path)
        self.session.commit()
        return document

    def process_document(self, document_id: int, local_file_path: str) -> None:
        document = self.session.get(Document, document_id)
        if document is None:
            raise ValueError("Document not found")

        text = self.ingestion.extract_text(local_file_path, document.mime_type)
        chunks = self.ingestion.chunk_text(text)
        document.chunk_count = len(chunks)
        document.status = "indexed"

        self.qdrant.upsert_chunks(
            company_id=document.company_id,
            document_id=document.id,
            chunks=chunks,
            metadata={
                "filename": document.filename,
                "knowledge_base_id": document.knowledge_base_id,
                "s3_key": document.s3_key,
            },
        )
