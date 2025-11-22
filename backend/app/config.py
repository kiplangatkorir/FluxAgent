import os
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    api_prefix: str = Field(default="/api")
    environment: str = Field(default=os.getenv("ENVIRONMENT", "local"))

    # Database
    postgres_host: str = Field(default=os.getenv("POSTGRES_HOST", "postgres"))
    postgres_port: int = Field(default=int(os.getenv("POSTGRES_PORT", "5432")))
    postgres_db: str = Field(default=os.getenv("POSTGRES_DB", "fluxagent"))
    postgres_user: str = Field(default=os.getenv("POSTGRES_USER", "postgres"))
    postgres_password: str = Field(
        default=os.getenv("POSTGRES_PASSWORD", "postgres")
    )
    pgvector_collection: str = Field(
        default=os.getenv("PGVECTOR_COLLECTION", "flux_documents")
    )

    # Langfuse
    langfuse_public_key: str = Field(
        default=os.getenv("LANGFUSE_PUBLIC_KEY", "public-placeholder")
    )
    langfuse_secret_key: str = Field(
        default=os.getenv("LANGFUSE_SECRET_KEY", "secret-placeholder")
    )
    langfuse_host: str = Field(
        default=os.getenv("LANGFUSE_HOST", "http://langfuse:3000")
    )

    # LLM Providers
    default_provider: str = Field(
        default=os.getenv("DEFAULT_LLM_PROVIDER", "ollama")
    )
    default_model: str = Field(
        default=os.getenv("DEFAULT_LLM_MODEL", "phi3")
    )
    openai_api_key: str = Field(default=os.getenv("OPENAI_API_KEY", ""))
    anthropic_api_key: str = Field(default=os.getenv("ANTHROPIC_API_KEY", ""))
    groq_api_key: str = Field(default=os.getenv("GROQ_API_KEY", ""))
    ollama_base_url: str = Field(
        default=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    )
    available_models: List[dict] = Field(
        default_factory=lambda: [
            {"provider": "ollama", "model": "phi3"},
            {"provider": "ollama", "model": "mistral:7b"},
            {"provider": "openai", "model": "gpt-4o-mini"},
            {"provider": "openai", "model": "gpt-4.1-mini"},
            {"provider": "anthropic", "model": "claude-3-haiku-20240307"},
            {"provider": "groq", "model": "llama3-70b-8192"},
        ]
    )

    # Embeddings
    embedding_model: str = Field(
        default=os.getenv(
            "EMBEDDING_MODEL", "text-embedding-3-large"
        )
    )

    storage_dir: str = Field(
        default=os.getenv("STORAGE_DIR", "/app/storage")
    )
    uploads_dir: str = Field(
        default=os.path.join(
            os.getenv("STORAGE_DIR", "/app/storage"), "uploads"
        )
    )
    mail_log_path: str = Field(
        default=os.path.join(
            os.getenv("STORAGE_DIR", "/app/storage"), "logs", "sent_mail.log"
        )
    )
    webhook_base_url: str = Field(
        default=os.getenv("WEBHOOK_BASE_URL", "https://webhook.site")
    )
    
    # File upload limits (in bytes: 10MB default)
    max_upload_size: int = Field(
        default=int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def psycopg_connection_string(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()

