import { useState, useCallback } from 'react'
import { sendChatMessage, ingestUrl as apiIngestUrl } from '../services/api'

/**
 * Custom hook for chat functionality
 */
export function useChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'bot',
      text: 'Namaste. I am Netra. I hold the wisdom of the Tantras. Ask me about mantras, meditation, or feed me knowledge from scripture URLs.',
      timestamp: new Date(),
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  /**
   * Add a message to the chat
   */
  const addMessage = useCallback((role, text) => {
    const newMessage = {
      id: Date.now(),
      role,
      text,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, newMessage])
    return newMessage
  }, [])

  /**
   * Send a chat message
   */
  const sendMessage = useCallback(async (question) => {
    setError(null)

    // Add user message
    addMessage('user', question)
    setIsLoading(true)

    try {
      const response = await sendChatMessage(question)

      // Format response with sources if available
      let responseText = response.response
      if (response.sources && response.sources.length > 0) {
        responseText += `\n\n📚 Sources: ${response.sources.join(', ')}`
      }

      addMessage('bot', responseText)
    } catch (err) {
      console.error('Chat error:', err)
      setError(err.message || 'Failed to get response')
      addMessage('bot', 'The connection to the Akasha is disrupted. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }, [addMessage])

  /**
   * Ingest a URL into the knowledge base
   */
  const ingestUrl = useCallback(async (url) => {
    setError(null)

    // Add user message showing URL
    addMessage('user', `📎 ${url}`)
    setIsLoading(true)

    try {
      const response = await apiIngestUrl(url)
      addMessage('bot', `✨ ${response.message}`)
    } catch (err) {
      console.error('Ingest error:', err)
      setError(err.message || 'Failed to ingest URL')
      addMessage('bot', 'I could not absorb wisdom from this source. The URL may be invalid or inaccessible.')
    } finally {
      setIsLoading(false)
    }
  }, [addMessage])

  /**
   * Clear error
   */
  const clearError = useCallback(() => {
    setError(null)
  }, [])

  /**
   * Clear chat history
   */
  const clearChat = useCallback(() => {
    setMessages([
      {
        id: Date.now(),
        role: 'bot',
        text: 'Namaste. I am Netra. I hold the wisdom of the Tantras. Ask me about mantras, meditation, or feed me knowledge from scripture URLs.',
        timestamp: new Date(),
      },
    ])
  }, [])

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    ingestUrl,
    clearError,
    clearChat,
  }
}
