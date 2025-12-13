/**
 * API client for Netra backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Send a chat message to Netra (non-streaming)
 * @param {string} question - The question to ask
 * @returns {Promise<{response: string, context_used: string, sources: string[]}>}
 */
export async function sendChatMessage(question) {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `HTTP error: ${response.status}`)
  }

  return response.json()
}

/**
 * Send a chat message with streaming response
 * @param {string} question - The question to ask
 * @param {function} onChunk - Callback for each text chunk
 * @param {function} onDone - Callback when streaming is complete (receives sources)
 * @param {function} onError - Callback for errors
 */
export async function sendChatMessageStream(question, onChunk, onDone, onError) {
  try {
    const response = await fetch(`${API_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail || `HTTP error: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      const lines = text.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.chunk) {
              onChunk(data.chunk)
            }
            if (data.done) {
              onDone(data.sources || [])
            }
            if (data.error) {
              onError(new Error(data.error))
            }
          } catch (e) {
            // Skip invalid JSON lines
          }
        }
      }
    }
  } catch (err) {
    onError(err)
  }
}

/**
 * Ingest a URL into the knowledge base
 * @param {string} url - The URL to ingest
 * @returns {Promise<{status: string, message: string, chunks_added: number}>}
 */
export async function ingestUrl(url) {
  const response = await fetch(`${API_URL}/learn`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `HTTP error: ${response.status}`)
  }

  return response.json()
}

/**
 * Get health status
 * @returns {Promise<{status: string, version: string, llm_provider: string}>}
 */
export async function getHealth() {
  const response = await fetch(`${API_URL}/health`)

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`)
  }

  return response.json()
}

/**
 * Get knowledge base statistics
 * @returns {Promise<{total_chunks: number, total_sources: number, collection_name: string}>}
 */
export async function getStats() {
  const response = await fetch(`${API_URL}/stats`)

  if (!response.ok) {
    throw new Error(`Stats fetch failed: ${response.status}`)
  }

  return response.json()
}
