import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    os.makedirs(settings.uploads_dir, exist_ok=True)
    os.makedirs(os.path.dirname(settings.mail_log_path), exist_ok=True)
    yield
    # Shutdown (if needed)
    pass


app = FastAPI(
    title="FluxAgent Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"message": "FluxAgent backend is running"}

