from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_user
from app.models.entities import User
from app.schemas.knowledge import DocumentRead, KnowledgeBaseCreate, KnowledgeBaseRead
from app.services.knowledge import KnowledgeService

router = APIRouter()


@router.post("/bases", response_model=KnowledgeBaseRead)
def create_knowledge_base(payload: KnowledgeBaseCreate, session: Session = Depends(db_session), current_user: User = Depends(get_current_user)) -> KnowledgeBaseRead:
    service = KnowledgeService(session)
    kb = service.create_knowledge_base(current_user.company_id, payload.name, payload.description, payload.is_default)
    return KnowledgeBaseRead.model_validate(kb)


@router.post("/bases/{knowledge_base_id}/documents", response_model=DocumentRead)
def upload_document(
    knowledge_base_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
) -> DocumentRead:
    service = KnowledgeService(session)
    try:
        document = service.upload_document(current_user.company_id, knowledge_base_id, current_user.id, file)
        return DocumentRead.model_validate(document)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc