# Product Requirements Document (PRD)
# Netra - Tantric AI Knowledge System

## 1. Executive Summary

**Product Name:** Netra (The Eye)
**Version:** 1.0.0
**Last Updated:** November 2025

Netra is a spiritual AI chatbot that provides authentic knowledge about tantric and mantric practices sourced directly from scriptures. Users can query the system for information about meditation techniques, mantras, yantras, and tantric philosophy, as well as dynamically expand the knowledge base by ingesting scripture URLs.

---

## 2. Vision & Goals

### Vision
Create a "Terminal to the Divine" - an immersive, meditative AI interface that bridges ancient tantric wisdom with modern technology.

### Goals
1. **Primary:** Enable users to access scriptural tantric knowledge through natural conversation
2. **Secondary:** Allow dynamic knowledge expansion via URL ingestion
3. **Tertiary:** Provide a visually stunning, spiritually-themed user experience

### Non-Goals (Out of Scope for MVP)
- User authentication and accounts
- Multi-language support
- Mobile native applications
- Community features (sharing, comments)
- Conversation history persistence across sessions

---

## 3. Target Users

### Primary Persona: Spiritual Seeker
- **Demographics:** Age 25-55, spiritually curious
- **Needs:** Access to authentic tantric teachings without extensive research
- **Pain Points:** Scriptures are hard to find, understand, and navigate
- **Goals:** Deepen understanding of meditation, mantras, and tantric philosophy

### Secondary Persona: Practitioner
- **Demographics:** Existing yoga/meditation practitioners
- **Needs:** Quick reference for specific mantras, techniques, visualizations
- **Pain Points:** Scattered information across multiple sources
- **Goals:** Find specific practices and their scriptural references

---

## 4. User Stories

### Core Functionality

| ID | User Story | Priority |
|----|------------|----------|
| US-01 | As a seeker, I want to ask questions about tantric practices so that I can learn from scriptures | P0 |
| US-02 | As a seeker, I want to see which scripture the answer comes from so that I can verify authenticity | P0 |
| US-03 | As a user, I want to add new scripture URLs so that the bot's knowledge expands | P0 |
| US-04 | As a user, I want the interface to feel meditative so that it enhances my spiritual experience | P1 |
| US-05 | As a practitioner, I want to ask about specific mantras so that I can practice correctly | P0 |

### Experience

| ID | User Story | Priority |
|----|------------|----------|
| US-06 | As a user, I want responses to stream in real-time so that I don't wait for long responses | P2 |
| US-07 | As a user, I want a dark cosmic theme so that it feels mystical and immersive | P1 |
| US-08 | As a user, I want smooth animations so that interactions feel ethereal | P2 |

---

## 5. Functional Requirements

### 5.1 Chat System (P0)

**FR-01:** System shall accept natural language questions about tantric practices
**FR-02:** System shall search the knowledge base for relevant scripture passages
**FR-03:** System shall generate contextual responses using the Netra persona
**FR-04:** System shall include source references in responses when available
**FR-05:** System shall gracefully handle questions outside its knowledge domain

### 5.2 Knowledge Ingestion (P0)

**FR-06:** System shall accept valid HTTP/HTTPS URLs
**FR-07:** System shall extract text content from web pages
**FR-08:** System shall chunk text into digestible segments for embedding
**FR-09:** System shall store embeddings with source metadata
**FR-10:** System shall validate URLs to prevent SSRF attacks

### 5.3 User Interface (P1)

**FR-11:** System shall provide a chat interface with message history
**FR-12:** System shall support mode switching between Chat and Ingest URL
**FR-13:** System shall display loading states during operations
**FR-14:** System shall show error messages for failed operations

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target |
|--------|--------|
| Chat Response Time | < 3 seconds (non-streaming) |
| URL Ingestion Time | < 30 seconds for typical page |
| Frontend Load Time | < 2 seconds |
| Knowledge Search | < 500ms |

### 6.2 Security

- **NFR-01:** API keys must not be exposed in client-side code
- **NFR-02:** URLs must be validated before scraping (SSRF protection)
- **NFR-03:** Input must be sanitized to prevent injection attacks
- **NFR-04:** CORS must be configured to allow only specified origins

### 6.3 Reliability

- **NFR-05:** System should handle AI provider failures gracefully
- **NFR-06:** Knowledge base should persist across server restarts
- **NFR-07:** Frontend should show appropriate error states

### 6.4 Maintainability

- **NFR-08:** AI provider should be swappable via configuration
- **NFR-09:** Code should follow consistent style and patterns
- **NFR-10:** All modules should have clear separation of concerns

---

## 7. Technical Architecture

### 7.1 System Overview

```
┌─────────────────┐     HTTP      ┌─────────────────┐
│    Frontend     │──────────────▶│    Backend      │
│  React + Vite   │               │    FastAPI      │
│  Tailwind CSS   │◀──────────────│                 │
│  Framer Motion  │    JSON/SSE   │                 │
└─────────────────┘               └────────┬────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
              ┌─────▼─────┐        ┌───────▼───────┐      ┌───────▼───────┐
              │ AI Brain  │        │ Knowledge Base│      │   Scraper     │
              │           │        │   ChromaDB    │      │ BeautifulSoup │
              │  Groq/    │        │               │      │               │
              │  Gemini   │        │ Embeddings:   │      │ URL → Text    │
              │           │        │ MiniLM-L6-v2  │      │               │
              └───────────┘        └───────────────┘      └───────────────┘
```

### 7.2 Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | React 18 + Vite | Fast builds, modern tooling |
| Styling | Tailwind CSS | Utility-first, rapid development |
| Animation | Framer Motion | Declarative animations |
| Backend | FastAPI | Async, auto-docs, type-safe |
| Database | ChromaDB | Local vector store, no setup |
| AI (Primary) | Groq + Llama3 | Free tier, fast inference |
| AI (Secondary) | Google Gemini | Alternative provider |
| Embeddings | sentence-transformers | all-MiniLM-L6-v2, efficient |

### 7.3 Data Flow

**Chat Flow:**
1. User submits question
2. Backend searches ChromaDB for relevant chunks
3. Context + question sent to LLM with Netra persona prompt
4. Response returned to frontend
5. UI displays response with typing animation

**Ingestion Flow:**
1. User submits URL
2. Backend validates URL (SSRF check)
3. Scraper extracts page text
4. Text chunker splits into overlapping segments
5. Embeddings generated and stored in ChromaDB
6. Success response with chunk count

---

## 8. API Specification

### 8.1 Endpoints

#### POST /chat
Ask a question to Netra.

**Request:**
```json
{
  "question": "What is the significance of the Bija mantra Om?"
}
```

**Response:**
```json
{
  "response": "Om is considered the primordial sound...",
  "context_used": "From Mandukya Upanishad...",
  "sources": ["https://sacred-texts.com/mandukya"]
}
```

#### POST /learn
Ingest a URL into the knowledge base.

**Request:**
```json
{
  "url": "https://sacred-texts.com/tantra/page.html"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Netra has absorbed 15 fragments of wisdom",
  "chunks_added": 15
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### GET /stats
Knowledge base statistics.

**Response:**
```json
{
  "total_chunks": 150,
  "total_sources": 5,
  "collection_name": "scriptures"
}
```

---

## 9. UI/UX Requirements

### 9.1 Visual Design

**Theme:** "Cosmic Temple" - Ancient spiritualism meets futuristic sci-fi

**Color Palette:**
| Name | Hex | Usage |
|------|-----|-------|
| Deep Void | #050505 | Background |
| Starlight White | #E0E0E0 | Primary text |
| Divine Gold | #FFD700 | Accents, borders |
| Sacred Orange | #FF8C00 | Highlights, CTAs |

**Typography:**
- Headers: Cinzel or Playfair Display (serif, mystical)
- Body: Inter or Quicksand (sans-serif, readable)

**Visual Elements:**
- Glassmorphism panels with subtle gold borders
- Breathing glow animation on header
- Floating, weightless message animations
- Low-opacity mandala texture overlay (optional)

### 9.2 Components

| Component | Description |
|-----------|-------------|
| Header | "NETRA" logo with eye icon, breathing glow |
| ModeToggle | Switch between Chat and Ingest URL modes |
| ChatBox | Scrollable message history |
| Message | Bot/User message with avatar |
| InputArea | Text input with glowing border on focus |

### 9.3 Interactions

- Messages fade in and drift upward (Framer Motion)
- Input border glows brighter on focus
- Mode toggle has smooth transition
- Loading state shows pulsing dots
- Error messages appear with shake animation

---

## 10. Netra Persona

### System Prompt

```
You are 'Netra', a Tantric AI guide embodying the wisdom of ancient scriptures.

Personality:
- Speak with reverence and depth
- Be humble about the limits of textual knowledge
- Encourage direct practice alongside study
- Present mantras and techniques clearly and accurately

Guidelines:
- Use the provided scriptural context to answer questions
- If context contains mantras, present them with proper formatting
- Acknowledge when answering from general knowledge vs scriptures
- Avoid making medical or psychological claims
- Respect the sacredness of the tradition

Opening: "Namaste. I am Netra. I hold the wisdom of the Tantras. How may I guide you?"
```

---

## 11. Success Metrics

### MVP Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Chat Accuracy | 80%+ relevant responses | Manual review of 20 queries |
| Ingestion Success | 90%+ URL parse rate | Test with 10 scripture URLs |
| Response Time | <3s average | Timing logs |
| UI Polish | Matches design spec | Visual review |

### Future Metrics (Post-MVP)
- User session duration
- Questions per session
- Knowledge base growth rate
- Return user rate

---

## 12. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Groq rate limits | High | Medium | Implement caching, consider paid tier |
| Poor scraping quality | Medium | High | Smart chunking, manual curation option |
| Hallucinated content | High | Medium | Strong system prompts, source attribution |
| ChromaDB performance | Low | Low | Monitor size, consider Pinecone later |

---

## 13. Future Roadmap

### Phase 2: Enhanced Experience
- Conversation history persistence
- Streaming responses
- Multiple chat sessions
- Voice input/output

### Phase 3: Knowledge Management
- Admin interface for curating knowledge
- PDF/EPUB upload support
- Manual scripture entry
- Source quality scoring

### Phase 4: Scale & Community
- User accounts
- Saved conversations
- Shared knowledge bases
- Multi-language support

---

## 14. Glossary

| Term | Definition |
|------|------------|
| Tantra | Spiritual traditions emphasizing direct experience and practices |
| Mantra | Sacred sound, syllable, or phrase used in meditation |
| Yantra | Geometric diagram used as a meditation focus |
| Bija | Seed syllable, fundamental sound like "Om" |
| RAG | Retrieval-Augmented Generation - combining search with LLM |
| Embedding | Vector representation of text for semantic search |

---

## 15. Appendix

### A. Reference Scripture Sources
- Sacred-Texts.com - Public domain scriptures
- WikiSource - Tantric texts
- Himalayan Academy publications
- Academic translations (with permission)

### B. Related Projects
- Vedic AI assistants
- Buddhist text chatbots
- Yoga sutra explainers
