# Quick Start Guide - FluxAgent

## ✅ **FIXES APPLIED**

1. ✅ **Dependency conflicts resolved** - Removed langchain-groq
2. ✅ **Package versions fixed** - langchain-postgres corrected
3. ✅ **TypeScript types fixed** - Added StepStatus type
4. ✅ **Path aliases configured** - Added @/* paths to tsconfig.json
5. ✅ **Public directory created** - Required by Next.js Dockerfile

## 🚀 **TO START THE SYSTEM**

### Step 1: Build and Start All Services
```powershell
docker compose up --build -d
```

This will:
- Build backend (Python/FastAPI)
- Build frontend (Next.js)
- Pull and start all database/services (Postgres, Langfuse stack)

**Expected time: 5-10 minutes** (first time)

### Step 2: Check Status
```powershell
docker compose ps
```

All services should show "Up" status.

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **API Docs**: http://localhost:8000/docs
- **Langfuse UI**: http://localhost:3001

### Step 4: Initialize Langfuse (First Time)

1. Go to http://localhost:3001
2. Sign in with credentials from `.env`:
   - Email: `admin@example.com`
   - Password: `changeme`
3. Create/confirm the project
4. Copy the public/secret keys to `.env`
5. Restart backend: `docker compose restart backend`

## 📝 **Quick Test**

1. **Upload a document**:
   - Go to http://localhost:3000/upload
   - Upload a PDF or TXT file

2. **Query the agent**:
   - Go to http://localhost:3000/query
   - Enter a question like: "Summarize the uploaded documents"
   - Select an LLM provider
   - Click "Run Agent"
   - View the timeline and RAG hits

## ⚠️ **IF ISSUES**

### Docker Desktop Not Running
- Start Docker Desktop application
- Wait for it to fully initialize

### Port Conflicts
If ports 3000, 8000, 3001, 5432 are in use, stop those services first.

### Build Fails
```powershell
# Clean and rebuild
docker compose down
docker compose build --no-cache
docker compose up -d
```

### View Logs
```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

## 🎯 **System Status**

- ✅ Backend: All 6 tools implemented
- ✅ Frontend: Timeline with icons, RAG display
- ✅ RAG: pgvector integration working
- ✅ LLM: 3 providers (Ollama, OpenAI, Anthropic)
- ✅ Docker: Full compose setup ready

