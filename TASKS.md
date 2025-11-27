# TASKS.md - NetraAI Development Tasks

Generated from PRD.md. Use this to track implementation progress.

## Phase 1: Foundation (Completed)

- [x] Create project directory structure
- [x] Set up backend with FastAPI
- [x] Configure pydantic-settings for environment variables
- [x] Add CORS middleware
- [x] Create .env.example files
- [x] Set up frontend with Vite + React
- [x] Configure Tailwind CSS with custom theme
- [x] Create PRD.md
- [x] Create CLAUDE.md

## Phase 2: Core Backend Services (Completed)

- [x] Implement LLMProvider abstract class
- [x] Create GroqProvider implementation
- [x] Create GeminiProvider implementation
- [x] Implement AIBrain orchestration layer
- [x] Create KnowledgeBase (ChromaDB wrapper)
- [x] Implement smart text chunking with overlap
- [x] Create web scraper with BeautifulSoup
- [x] Add URL validation (SSRF protection)

## Phase 3: API Layer (Completed)

- [x] Create Pydantic schemas for requests/responses
- [x] Implement POST /chat endpoint
- [x] Implement POST /learn endpoint
- [x] Add GET /health endpoint
- [x] Add GET /stats endpoint
- [x] Add error handling

## Phase 4: Frontend (Completed)

- [x] Create Header component with breathing glow
- [x] Create ModeToggle component
- [x] Create ChatBox with auto-scroll
- [x] Create Message component with animations
- [x] Create InputArea component
- [x] Implement useChat hook
- [x] Create API service client
- [x] Add global CSS with cosmic theme

## Phase 5: Integration (Completed)

- [x] Connect frontend to backend APIs
- [x] Handle loading states
- [x] Handle error states
- [x] Test chat flow end-to-end
- [x] Test URL ingestion flow

## Phase 6: Documentation (Completed)

- [x] Write README.md
- [x] Create docs/API.md
- [x] Generate TASKS.md from PRD
- [x] Document environment variables

---

## Future Enhancements (Backlog)

### Streaming Responses
- [ ] Add /chat/stream endpoint with SSE
- [ ] Implement streaming in GroqProvider
- [ ] Update frontend to handle streaming
- [ ] Add typing indicator during stream

### Conversation History
- [ ] Add session_id to chat requests
- [ ] Implement server-side session storage
- [ ] Pass history to LLM for context
- [ ] Add "clear chat" functionality
- [ ] Consider Redis for production

### Enhanced Knowledge Management
- [ ] Add PDF upload support
- [ ] Add EPUB support
- [ ] Manual text entry interface
- [ ] Source quality scoring
- [ ] Deduplication logic

### Performance & Reliability
- [ ] Add response caching
- [ ] Implement rate limiting (slowapi)
- [ ] Add structured logging
- [ ] Create health check dashboard
- [ ] Add metrics collection

### User Experience
- [ ] Add dark/light theme toggle
- [ ] Voice input support
- [ ] Voice output (TTS)
- [ ] Mobile-responsive improvements
- [ ] Keyboard shortcuts

### Security
- [ ] Add basic authentication
- [ ] Input sanitization review
- [ ] Security headers
- [ ] Content Security Policy

### DevOps
- [ ] Docker containerization
- [ ] Docker Compose setup
- [ ] CI/CD pipeline
- [ ] Production deployment guide

---

## Quick Reference

### Running Locally

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

### Testing

```bash
# Backend tests
cd backend && pytest

# Manual API test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Om?"}'
```

### Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI entry point |
| `backend/app/config.py` | Environment configuration |
| `backend/app/services/ai_brain.py` | LLM orchestration |
| `backend/app/services/knowledge_base.py` | ChromaDB wrapper |
| `frontend/src/App.jsx` | Main React component |
| `frontend/src/hooks/useChat.js` | Chat state management |
