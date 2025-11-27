# Netra API Documentation

Base URL: `http://localhost:8000`

## Authentication

No authentication required for MVP.

## Endpoints

### POST /chat

Ask Netra a question about tantric practices.

**Request Body:**
```json
{
  "question": "What is the significance of the Om mantra?"
}
```

**Response:**
```json
{
  "response": "Om is considered the primordial sound from which all creation emerged...",
  "context_used": "From the Mandukya Upanishad: Om represents the three states of consciousness...",
  "sources": ["https://sacred-texts.com/mandukya"]
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid request
- `500` - Server error

---

### POST /learn

Ingest a URL into the knowledge base.

**Request Body:**
```json
{
  "url": "https://sacred-texts.com/tantra/page.html"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Netra has absorbed 15 fragments of wisdom from this source",
  "chunks_added": 15
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid URL or insufficient content
- `500` - Server error

**Notes:**
- URL must be publicly accessible HTTP/HTTPS
- Private/internal URLs are blocked for security
- Minimum content length: 100 characters

---

### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "llm_provider": "groq"
}
```

---

### GET /stats

Get knowledge base statistics.

**Response:**
```json
{
  "total_chunks": 150,
  "total_sources": 5,
  "collection_name": "scriptures"
}
```

---

## Error Handling

All errors return JSON with a `detail` field:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common error codes:
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

---

## Rate Limiting

Default: 60 requests per minute per IP.

When rate limited, you'll receive:
```json
{
  "detail": "Rate limit exceeded. Try again in X seconds."
}
```

---

## Examples

### cURL

**Chat:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is tantra?"}'
```

**Learn:**
```bash
curl -X POST http://localhost:8000/learn \
  -H "Content-Type: application/json" \
  -d '{"url": "https://sacred-texts.com/hin/vbh/vbh01.htm"}'
```

**Health:**
```bash
curl http://localhost:8000/health
```

### Python

```python
import requests

# Chat
response = requests.post(
    "http://localhost:8000/chat",
    json={"question": "What is the Bija mantra Om?"}
)
print(response.json())

# Learn
response = requests.post(
    "http://localhost:8000/learn",
    json={"url": "https://sacred-texts.com/tantra/page.html"}
)
print(response.json())
```

### JavaScript

```javascript
// Chat
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'What is tantra?' })
});
const data = await response.json();
console.log(data);
```

---

## OpenAPI Schema

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
