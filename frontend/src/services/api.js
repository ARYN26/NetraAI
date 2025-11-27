/**
 * API client for Netra backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Send a chat message to Netra
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
