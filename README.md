# FluxAgent

FluxAgent is a full-stack AI Agent reference implementation designed to demonstrate a multi-tool, multi-LLM agent with RAG, observability (Langfuse), and an approachable UI.

**What it does**
- Upload documents and index them into Postgres/pgvector.
- Run a LangChain-based agent that reasons in multiple steps and can call tools (search, calculator, RAG lookup, SQL reader, HTTP webhook, mock mail).
- Switch between multiple LLM providers/models (OpenAI, Anthropic, Ollama, optionally Groq).
- Log prompts, completions, and tool calls to Langfuse for LLMOps.
- Inspect an execution timeline (icons for pending / in-progress / done / error) and view RAG hits.

**Repository layout**
- `backend/` — FastAPI application and LangChain agent.
- `frontend/` — Next.js 14 UI (upload + query + timeline components).
- `docker-compose.yml` — Orchestrates backend, frontend, Postgres/pgvector, and Langfuse stack.
- `env.example` — Example environment variables used by the app and Langfuse.
- `storage/` — Local mount for uploads and logs (used by the backend container).

**Highlights**
- Multi-LLM support (select provider + model per request)
- Tool-enabled agent (search, calculator, RAG, SQL, mail, HTTP)
- Langfuse integration for observability
- Single-command local reproduction with Docker Compose

**Quick prerequisites**
- Docker Desktop (Compose v2)
- Recommended: Ollama running on the host for offline/local LLMs: `ollama serve` and at least one model pulled (e.g., `phi3`).
- ~8–16 GB RAM recommended for the full stack.

**Quick start (full stack)**
1. Copy the environment template and edit `.env` as needed:

```powershell
cd c:/Users/Barchok/FluxAgent
Copy-Item env.example .env
# Edit `.env` to add API keys (OpenAI, Anthropic), and Langfuse init credentials.
```

2. (Optional) Prepare Ollama models on the host machine:

```powershell
# From a host terminal (PowerShell / WSL if installed)
ollama pull phi3
ollama pull mistral:7b
# Start the Ollama server if you use it locally:
ollama serve
```

3. Start the full stack with Docker Compose:

```powershell
docker compose up --build
```

Services (default ports)
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/api` (Swagger UI: `http://localhost:8000/docs`)
- Langfuse UI: `http://localhost:3001` (if Langfuse is enabled)
- MinIO console (Langfuse uploads): `http://localhost:9090`

**Langfuse initialization (explicit)**
1. Launch the entire stack (see Quick start).
2. Open the Langfuse web UI: `http://localhost:3001`.
3. Sign in using the seeded admin user defined in `env.example` (`LANGFUSE_INIT_USER_EMAIL`, `LANGFUSE_INIT_USER_PASSWORD`).
4. Create or open a project in Langfuse and copy the project's Public and Secret keys.
5. Add these keys to your `.env`:

```text
LANGFUSE_PUBLIC_KEY=<your_public_key_here>
LANGFUSE_SECRET_KEY=<your_secret_key_here>
LANGFUSE_HOST=http://langfuse-web:3001
```

6. Restart the backend so Langfuse callbacks start sending events:

```powershell
docker compose restart backend
```

Notes:
- The backend only instantiates Langfuse callbacks when real keys are present in `.env` (placeholder values are ignored).
- If you change Langfuse keys, restart the backend container to pick up the changes.

**Multi-LLM switching (UI & API)**
- The frontend exposes a provider/model dropdown on the query page. Choose an LLM provider (e.g., `ollama`, `openai`, `anthropic`) and a model before sending a query.
- API example: `POST /api/agent/query` accepts JSON with optional `provider` and `model` fields. Example request body:

```json
{
  "query": "Summarize the uploaded docs and compute the sum of 12+34.",
  "provider": "ollama",
  "model": "phi3"
}
```

Example response (important fields):

```json
{
  "final_answer": "...agent's final output...",
  "steps": [ /* timeline steps with status and tool outputs */ ],
  "rag_hits": [ /* retrieved documents */ ],
  "provider": "ollama",
  "model": "phi3"
}
```

If `provider`/`model` are omitted, the backend falls back to defaults defined in the app settings.

**Agent tools (what they do)**
- Search tool (mock): Returns canned search results for demo purposes.
- Calculator: Evaluates arithmetic expressions locally (safe, no external calls).
- Document RAG lookup: Uses `pgvector` embeddings to retrieve context from uploaded docs.
- Send-mail (mock): Logs outgoing mail to a file (no real emails sent).
- HTTP tool: Performs GET/POST to target URLs (useful with webhook.site for testing).
- SQL fetch tool: Runs read-only queries against a seeded Postgres table (example dataset in the repo).

Tool behavior notes
- All tool calls are recorded in the agent timeline and (when enabled) forwarded to Langfuse for observability.
- The timeline records tool start/end, outputs, and errors, and the frontend renders icons and collapsible steps.

**Document upload & RAG**
- Upload documents from the frontend (`/upload`) or via API `POST /api/documents/upload` (multipart form file field `file`).
- The backend extracts text (PDF/text), splits into chunks, embeds them, and stores vectors in Postgres/pgvector.

Sample upload flow (API):

```powershell
curl -F "file=@./sample.pdf" http://localhost:8000/api/documents/upload
```

**Local development**
- Backend (fast reload):

```powershell
cd backend
# Create a virtualenv and install requirements, or use the docker container
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Frontend (Next.js):

```powershell
cd frontend
npm install
npm run dev
```

**API endpoints (summary)**
- `GET /api/health` — basic health
- `GET /api/models` — returns available model/provider options
- `POST /api/documents/upload` — upload + index a document (multipart file)
- `POST /api/agent/query` — run agent; body: `{ query, provider?, model? }`

**Troubleshooting & tips**
- If using Ollama on Windows, ensure `ollama serve` is reachable from containers. The repo assumes the host is reachable at `http://host.docker.internal:11434`.
- If Langfuse events do not appear in the UI, verify `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` in `.env` and restart the backend.
- Check uploaded files and mail logs under `./storage/uploads` and `./storage/logs` respectively.

**Testing the agent quickly**
1. Upload a small text file via the UI or `POST /api/documents/upload`.
2. On the query page select a provider/model and submit a question that references the uploaded content.
3. Inspect the timeline for tool calls and RAG hits; open Langfuse to view searchable traces.

**Contributing / Evaluation checklist**
- The system demonstrates multiple LLM providers, RAG with pgvector, all six tools, Langfuse instrumentation, and a usable UI with timeline traces.
- For a technical test submission, ensure `docker-compose.yml`, `env.example`, and this README are present and the full project is pushed to GitHub.

--
If you'd like, I can now:
- Add a short `curl` example that exercises the `agent/query` endpoint with provider/model.
- Create a tiny seed script to insert sample documents into pgvector for quick demo.
- Walk through starting the stack on your machine and confirm Langfuse keys.
Tell me which next step you prefer.

