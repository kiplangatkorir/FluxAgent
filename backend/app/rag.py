import os
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    OpenAIEmbeddings = None

from langchain_postgres import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings

from .config import get_settings

settings = get_settings()

_embedding_model = None
_vector_store = None


def _resolve_embedding_model():
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model

    if settings.openai_api_key and OpenAIEmbeddings:
        _embedding_model = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
        )
    else:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embedding_model


def get_vector_store() -> PGVector:
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    embeddings = _resolve_embedding_model()
    _vector_store = PGVector(
        embeddings=embeddings,
        connection_string=settings.psycopg_connection_string,
        collection_name=settings.pgvector_collection,
        use_jsonb=True,
    )
    return _vector_store


def ingest_document(content: str, metadata: dict) -> int:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
    )
    docs: List[Document] = [
        Document(page_content=chunk, metadata=metadata)
        for chunk in text_splitter.split_text(content)
    ]
    if not docs:
        return 0
    store = get_vector_store()
    store.add_documents(docs)
    return len(docs)


def similarity_search(query: str, k: int = 4) -> List[Document]:
    store = get_vector_store()
    return store.similarity_search(query, k=k)


def load_text_from_upload(file_path: str, content_type: str) -> str:
    path = Path(file_path)
    if content_type == "application/pdf" or path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("pypdf is required to process PDF files") from exc

        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    with open(path, "r", encoding="utf-8", errors="ignore") as handler:
        return handler.read()

