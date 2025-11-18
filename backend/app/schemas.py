from typing import List, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class DocumentUploadResponse(BaseModel):
    document_id: int
    chunks_indexed: int
    filename: str


class ChatRequest(BaseModel):
    query: str
    provider: Optional[str] = None
    model: Optional[str] = None


class TimelineStep(BaseModel):
    id: str
    name: str
    type: str
    status: str
    input: Optional[str] = None
    output: Optional[str] = None


class RagHit(BaseModel):
    content: str
    metadata: dict


class ChatResponse(BaseModel):
    final_answer: str
    steps: List[TimelineStep]
    rag_hits: List[RagHit]
    provider: str
    model: str


class ModelOption(BaseModel):
    provider: str
    model: str


class ModelListResponse(BaseModel):
    options: List[ModelOption]

