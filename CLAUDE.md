# CLAUDE.md - NetraAI Project Guide

## Project Overview

**Netra** is a Tantric AI chatbot that provides knowledge of tantric/mantric practices from scriptures. It uses RAG (Retrieval-Augmented Generation) to ground responses in actual scriptural text.

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env  # Add your GROQ_API_KEY
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Architecture

```
NetraAI/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── main.py         # Entry point, CORS, lifespan
│   │   ├── config.py       # Environment config (pydantic-settings)
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic modules
│   │   │   ├── ai_brain.py       # LLM orchestration
│   │   │   ├── groq_provider.py  # Groq implementation
│   │   │   ├── knowledge_base.py # ChromaDB wrapper
│   │   │   └── scraper.py        # URL text extraction
│   │   ├── api/            # Route handlers
│   │   └── utils/          # Helpers (chunking, validation)
│   └── tests/
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API client
│   │   └── styles/         # Global CSS
│   └── ...
└── docs/                   # Additional documentation
```

## Key Concepts

### RAG Pipeline
1. User asks question
2. Question embedded and searched against ChromaDB
3. Top-k relevant scripture chunks retrieved
4. Chunks + question sent to LLM with Netra persona
5. Response returned with source attribution

### Modular AI Provider
The `LLMProvider` abstract class allows swapping AI backends:
- `GroqProvider` - Default, uses Llama3-8b
- `GeminiProvider` - Alternative, Google's model

Switch via `LLM_PROVIDER` env var.

## Coding Standards

### Python (Backend)

**Style:**
- Follow PEP 8
- Use type hints everywhere
- Max line length: 100 characters
- Use `loguru` for logging

**Naming:**
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

**Imports:**
```python
# Standard library
import os
from typing import List, Optional

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local
from app.config import settings
from app.services.ai_brain import AIBrain
```

**Error Handling:**
```python
# Use specific exceptions
try:
    result = await knowledge_base.search(query)
except ChromaDBError as e:
    logger.error(f"Knowledge base search failed: {e}")
    raise HTTPException(status_code=500, detail="Search failed")
```

**Async Patterns:**
- Use `async/await` for I/O operations
- Use `BackgroundTasks` for non-blocking operations
- Avoid blocking calls in async functions

### JavaScript/React (Frontend)

**Style:**
- Use functional components with hooks
- Use ES6+ features (arrow functions, destructuring)
- Prefer `const` over `let`

**Naming:**
- Components: `PascalCase`
- Functions/variables: `camelCase`
- CSS classes: `kebab-case` or Tailwind utilities

**Component Structure:**
```jsx
// Imports
import { useState } from 'react';
import { motion } from 'framer-motion';

// Component
export function ChatMessage({ message, isBot }) {
  // Hooks first
  const [isVisible, setIsVisible] = useState(true);

  // Derived values
  const avatarIcon = isBot ? '👁' : '👤';

  // Render
  return (
    <motion.div className={`msg ${isBot ? 'bot' : 'user'}`}>
      {/* ... */}
    </motion.div>
  );
}
```

**State Management:**
- Use React hooks for local state
- Lift state up when needed
- No external state library for MVP

## File Templates

### New Service (Python)
```python
"""Service description."""
from loguru import logger
from app.config import settings


class MyService:
    """Service class description."""

    def __init__(self):
        """Initialize the service."""
        self._setup()

    def _setup(self):
        """Private setup method."""
        pass

    async def do_something(self, input: str) -> str:
        """
        Public method description.

        Args:
            input: Description of input

        Returns:
            Description of return value

        Raises:
            ValueError: When input is invalid
        """
        logger.debug(f"Processing: {input}")
        return result
```

### New Component (React)
```jsx
import { motion } from 'framer-motion';
import clsx from 'clsx';

/**
 * Component description
 * @param {Object} props
 * @param {string} props.requiredProp - Description
 * @param {boolean} [props.optionalProp=false] - Description
 */
export function MyComponent({ requiredProp, optionalProp = false }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={clsx(
        'base-classes',
        optionalProp && 'conditional-classes'
      )}
    >
      {requiredProp}
    </motion.div>
  );
}
```

## Environment Variables

### Backend (.env)
```bash
# Required
GROQ_API_KEY=gsk_...

# Optional
GOOGLE_API_KEY=           # For Gemini provider
LLM_PROVIDER=groq         # groq or gemini
CHROMA_DB_PATH=./netra_db
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
```

## Common Commands

```bash
# Backend
uvicorn app.main:app --reload          # Dev server
pytest                                  # Run tests
pip freeze > requirements.txt          # Update deps

# Frontend
npm run dev                            # Dev server
npm run build                          # Production build
npm run lint                           # Lint code
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Ask Netra a question |
| POST | `/learn` | Ingest URL into knowledge base |
| GET | `/health` | Health check |
| GET | `/stats` | Knowledge base statistics |

## Troubleshooting

### CORS Errors
Ensure `CORS_ORIGINS` in backend `.env` matches frontend URL.

### ChromaDB Issues
Delete `netra_db/` folder to reset the knowledge base.

### Groq Rate Limits
Free tier has limits. Consider caching frequent queries.

### Embedding Model Download
First run downloads `all-MiniLM-L6-v2` (~90MB). Ensure internet connection.

## Design Decisions

1. **ChromaDB over Supabase** - Local, no account needed, fast prototyping
2. **Groq over OpenAI** - Free tier, fast Llama3, good for MVP
3. **No auth for MVP** - Reduces complexity, add later if needed
4. **No conversation history** - Simpler initial implementation
5. **Smart chunking** - Overlapping chunks preserve context

## References

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Groq API](https://console.groq.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)
