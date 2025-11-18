import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from .agent import run_agent
from .config import get_settings
from .database import SessionLocal, documents_table, init_db
from .rag import ingest_document, load_text_from_upload
from .schemas import (
    ChatRequest,
    ChatResponse,
    DocumentUploadResponse,
    HealthResponse,
    ModelListResponse,
)

router = APIRouter()
settings = get_settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
def on_startup():
    init_db()
    os.makedirs(settings.uploads_dir, exist_ok=True)
    os.makedirs(os.path.dirname(settings.mail_log_path), exist_ok=True)


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")


@router.get("/models", response_model=ModelListResponse)
def list_models():
    return ModelListResponse(options=settings.available_models)


@router.post(
    "/documents/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    stored_path = os.path.join(settings.uploads_dir, file.filename)
    with open(stored_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    content = load_text_from_upload(stored_path, file.content_type or "text/plain")
    metadata = {"filename": file.filename, "content_type": file.content_type}
    chunks = ingest_document(content, metadata)

    with SessionLocal() as session:
        stmt = (
            insert(documents_table)
            .values(
                original_filename=file.filename,
                stored_path=stored_path,
                content_type=file.content_type or "text/plain",
                metadata=metadata,
            )
            .returning(documents_table.c.id)
        )
        result = session.execute(stmt)
        session.commit()
        document_id = result.scalar_one()

    return DocumentUploadResponse(
        document_id=document_id,
        chunks_indexed=chunks,
        filename=file.filename,
    )


@router.post(
    "/agent/query",
    response_model=ChatResponse,
)
async def query_agent(payload: ChatRequest):
    if not payload.query:
        raise HTTPException(status_code=400, detail="Query is required.")

    result = run_agent(payload.query, payload.provider, payload.model)
    return ChatResponse(**result)

