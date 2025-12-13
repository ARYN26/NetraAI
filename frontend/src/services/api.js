/**
 * API client for Netra backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Default request timeout (30 seconds)
const REQUEST_TIMEOUT_MS = 30000

/**
 * Fetch with timeout support
 * @param {string} url - URL to fetch
 * @param {object} options - Fetch options
 * @param {number} timeoutMs - Timeout in milliseconds
 * @returns {Promise<Response>}
 */
async function fetchWithTimeout(url, options = {}, timeoutMs = REQUEST_TIMEOUT_MS) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    })
    return response
  } finally {
    clearTimeout(timeoutId)
  }
}

/**
 * Send a chat message to Netra (non-streaming)
 * @param {string} question - The question to ask
 * @returns {Promise<{response: string, context_used: string, sources: string[]}>}
 */
export async function sendChatMessage(question) {
  try {
    const response = await fetchWithTimeout(`${API_URL}/chat`, {
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
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.')
    }
    throw err
  }
}

/**
 * Send a chat message with streaming response
 * @param {string} question - The question to ask
 * @param {function} onChunk - Callback for each text chunk
 * @param {function} onDone - Callback when streaming is complete (receives sources)
 * @param {function} onError - Callback for errors
 * @param {AbortSignal} signal - Optional abort signal for cancellation
 */
export async function sendChatMessageStream(question, onChunk, onDone, onError, signal = null) {
  try {
    const response = await fetch(`${API_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
      signal,
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
    if (err.name === 'AbortError') {
      // User cancelled - not an error, just return silently
      return
    }
    onError(err)
  }
}

/**
 * Ingest a URL into the knowledge base
 * @param {string} url - The URL to ingest
 * @returns {Promise<{status: string, message: string, chunks_added: number}>}
 */
export async function ingestUrl(url) {
  try {
    // Longer timeout for URL ingestion (60 seconds)
    const response = await fetchWithTimeout(`${API_URL}/learn`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    }, 60000)

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail || `HTTP error: ${response.status}`)
    }

    return response.json()
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.')
    }
    throw err
  }
}

/**
 * Get health status
 * @returns {Promise<{status: string, version: string, llm_provider: string}>}
 */
export async function getHealth() {
  try {
    const response = await fetchWithTimeout(`${API_URL}/health`, {}, 10000)

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`)
    }

    return response.json()
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Health check timed out')
    }
    throw err
  }
}

/**
 * Get knowledge base statistics
 * @returns {Promise<{total_chunks: number, total_sources: number, collection_name: string}>}
 */
export async function getStats() {
  try {
    const response = await fetchWithTimeout(`${API_URL}/stats`)

    if (!response.ok) {
      throw new Error(`Stats fetch failed: ${response.status}`)
    }

    return response.json()
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Stats request timed out')
    }
    throw err
  }
}
