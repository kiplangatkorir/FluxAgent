import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from .agent import run_agent
from .config import get_settings
from .database import SessionLocal, documents_table
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

    stored_path = None
    try:
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.max_upload_size:
            max_size_mb = settings.max_upload_size / (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail=f"File size ({file_size / (1024 * 1024):.2f}MB) exceeds maximum allowed size ({max_size_mb:.2f}MB)."
            )
        
        # Validate file extension/content type
        allowed_extensions = {".pdf", ".txt", ".md"}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{file_ext}' not supported. Allowed types: {', '.join(allowed_extensions)}"
            )

        stored_path = os.path.join(settings.uploads_dir, file.filename)
        
        # Handle filename collisions
        if os.path.exists(stored_path):
            base, ext = os.path.splitext(file.filename)
            counter = 1
            while os.path.exists(stored_path):
                new_filename = f"{base}_{counter}{ext}"
                stored_path = os.path.join(settings.uploads_dir, new_filename)
                counter += 1
        
        with open(stored_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        content = load_text_from_upload(stored_path, file.content_type or "text/plain")
        if not content.strip():
            raise HTTPException(
                status_code=400,
                detail="File appears to be empty or could not be processed."
            )
        
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
    except HTTPException:
        raise
    except Exception as e:
        # Clean up file if it was created but processing failed
        if stored_path and os.path.exists(stored_path):
            try:
                os.remove(stored_path)
            except Exception:
                pass
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post(
    "/agent/query",
    response_model=ChatResponse,
)
async def query_agent(payload: ChatRequest):
    if not payload.query:
        raise HTTPException(status_code=400, detail="Query is required.")
    
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        result = run_agent(payload.query, payload.provider, payload.model)
        return ChatResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"LLM provider connection error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )

