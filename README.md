# Netra - The Eye of Tantric Wisdom

A spiritual AI guide that provides authentic knowledge about tantric practices, mantras, and meditation techniques sourced from scriptures.



## Features

- **Scripture-based Q&A**: Ask about tantric practices, mantras, meditation, yoga, and spiritual teachings
- **Topic Guardrails**: Only answers spiritual/tantric questions, rejects off-topic queries
- **RAG Architecture**: Responses grounded in actual scripture with source attribution
- **Guru Diksha Disclaimer**: Warns users to seek proper initiation before practicing
- **Conversation History**: Local storage of chat sessions with clear history option

## Tech Stack

- **Backend**: FastAPI + ChromaDB + Groq (Llama 3.1)
- **Frontend**: React + Vite + Tailwind CSS
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Groq API Key (free at [console.groq.com](https://console.groq.com/))

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: http://localhost:5173

### 3. Open the App

Visit http://localhost:5173 in your browser.

The knowledge base auto-seeds with scripture content on first run.

## Sample Questions

- "What is the significance of Om Namah Shivaya?"
- "How do I perform an 11-day Shiva anusthan?"
- "Explain the 112 meditation techniques from Vijnana Bhairava"
- "What is the proper vidhi for mantra japa?"

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key (required) | - |
| `LLM_PROVIDER` | AI provider (`groq` or `gemini`) | `groq` |
| `GROQ_MODEL` | Groq model name | `llama-3.1-8b-instant` |
| `CHROMA_DB_PATH` | ChromaDB storage path | `./netra_db` |
| `RELEVANCE_THRESHOLD` | Off-topic rejection threshold | `0.7` |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Ask a question |
| GET | `/health` | Health check |
| GET | `/stats` | Knowledge base stats |

## Project Structure

```
NetraAI/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry + auto-seeding
│   │   ├── config.py         # Environment config
│   │   ├── api/routes.py     # API endpoints
│   │   └── services/         # AI Brain, Knowledge Base
│   ├── scriptures/           # Scripture text files
│   └── scripts/              # Seeding scripts
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/            # useConversations hook
│   │   └── services/         # API client
│   └── package.json
└── README.md
```

## License

MIT
