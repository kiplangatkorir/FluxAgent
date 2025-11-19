#!/usr/bin/env python3
"""CLI entry point for database initialization."""
import sys
from app.database import init_db

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init_db":
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")
    else:
        print("Usage: python cli.py init_db")

