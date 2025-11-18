from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker

from .config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

metadata = MetaData(schema=None)

documents_table = Table(
    "documents",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("original_filename", String(255), nullable=False),
    Column("stored_path", String(512), nullable=False),
    Column("content_type", String(64), nullable=False),
    Column("uploaded_by", String(128), nullable=True),
    Column("metadata", JSONB, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    ),
)

support_table = Table(
    "support_records",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("account_name", String(128), nullable=False),
    Column("priority", String(32), nullable=False),
    Column("status", String(32), nullable=False),
    Column("summary", Text, nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    ),
)


def init_db() -> None:
    metadata.create_all(bind=engine)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        result = conn.execute(text("SELECT COUNT(*) FROM support_records"))
        count = result.scalar_one()
        if count == 0:
            seed_data = [
                {
                    "account_name": "Acme Corp",
                    "priority": "high",
                    "status": "open",
                    "summary": "Payment gateway timeout for EU customers.",
                },
                {
                    "account_name": "Globex",
                    "priority": "medium",
                    "status": "open",
                    "summary": "Analytics export missing two columns.",
                },
                {
                    "account_name": "Initech",
                    "priority": "low",
                    "status": "closed",
                    "summary": "Requested sandbox reset completed.",
                },
            ]
            for record in seed_data:
                conn.execute(
                    text(
                        """
                        INSERT INTO support_records (account_name, priority, status, summary, created_at)
                        VALUES (:account_name, :priority, :status, :summary, :created_at)
                        """
                    ),
                    {**record, "created_at": datetime.utcnow()},
                )

