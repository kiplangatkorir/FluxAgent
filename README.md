# FluxAgent

Full-stack AI agent platform with FastAPI, LangChain, pgvector retrieval, Langfuse observability, and a Next.js frontend. Users can upload documents, run multi-step agent workflows, inspect tool traces, and switch between multiple LLM providers.

## Architecture
- **Backend (`backend/`)** – FastAPI + LangChain agent with tools (mock search, calculator, RAG lookup, SQL reader, HTTP webhook, send-mail). Uses Postgres/pgvector for document storage and exposes `/api` endpoints.
- **Frontend (`frontend/`)** – Next.js 14 app (upload + query consoles) that renders the timeline view with status icons and RAG evidence.
- **Data layer** – Postgres with pgvector extension for embeddings plus seeded support tickets for SQL tool demos.
- **Langfuse** – Self-hosted stack (web UI + worker + Postgres + ClickHouse + MinIO + Redis) for logging prompts, completions, and tool invocations.
- **Docker** – `docker-compose.yml` orchestrates backend, frontend, Postgres, and the Langfuse stack so `docker compose up` runs the entire system.

## Prerequisites
- Docker Desktop (with Compose v2)
- Ollama running on the host (`ollama serve`) with at least one model pulled (default `phi3`)
- 16 GB RAM recommended (Langfuse stack + pgvector + frontend/backend)

## Quickstart
1. **Copy environment template**
   ```powershell
   cd FluxAgent
   Copy-Item env.example .env
   ```
   Update `.env` with any secrets (OpenAI keys, Langfuse passwords, etc.). The defaults are fine for local demos.

2. **Prep Ollama models (host machine)**
   ```bash
   ollama pull phi3
   ollama pull deepseek-r1:6.7b
   ```
   Leave `ollama serve` running so the backend can reach it via `http://host.docker.internal:11434`.

3. **Start the full stack**
   ```bash
   docker compose up --build
   ```
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Langfuse UI: http://localhost:3001
   - MinIO console (for Langfuse uploads): http://localhost:9090

4. **Initialize Langfuse**
   - Sign in using the credentials from `.env` (`LANGFUSE_INIT_USER_EMAIL`, etc.).
   - Create or confirm the auto-generated project.
   - Copy the project’s public/secret keys into `.env` (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`).
   - Restart the backend container (`docker compose restart backend`) so Langfuse logging activates.

5. **Use the app**
   - Upload PDFs/TXT files on `/upload`.
   - Ask multi-step questions on `/query`, pick models via the dropdown, and inspect the execution timeline + RAG matches.

## Service Overview
| Service | Port | Notes |
|---------|------|-------|
| `frontend` | 3000 | Next.js UI |
| `backend` | 8000 | FastAPI + LangChain agent |
| `postgres` | 5432 | App database with pgvector |
| `langfuse-web` | 3001 | Langfuse UI & ingestion endpoint |
| `langfuse-worker` | internal | Processes Langfuse events |
| `langfuse-clickhouse` | 8123/9000 (internal) | Langfuse analytics DB |
| `langfuse-postgres` | internal | Langfuse metadata DB |
| `langfuse-minio` | 9090 | Object storage for Langfuse uploads |
| `langfuse-redis` | internal | Queue for Langfuse |

App uploads/logs are stored under `./storage` (mounted into the backend container).

## Development Tips
- **Backend (local dev)**:
  ```bash
  cd backend
  uvicorn app.main:app --reload
  ```
- **Frontend (local dev)**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
- **Testing APIs** – Visit `http://localhost:8000/docs` for FastAPI Swagger UI.

## Deployment
- Update `.env` for production secrets and remote providers.
- Ensure Ollama or alternative LLM endpoints are reachable from the backend container.
- Push to GitHub along with `docker-compose.yml`, `env.example`, and this README so reviewers can run `docker compose up --build` to reproduce the entire system.

