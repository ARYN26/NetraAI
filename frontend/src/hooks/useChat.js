import { useState, useCallback, useRef } from 'react'
import { sendChatMessageStream, ingestUrl as apiIngestUrl } from '../services/api'

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
  const streamingMessageId = useRef(null)

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
   * Update a message by ID
   */
  const updateMessage = useCallback((id, text) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, text } : msg))
    )
  }, [])

  /**
   * Send a chat message with streaming
   */
  const sendMessage = useCallback(async (question) => {
    setError(null)

    // Add user message
    addMessage('user', question)
    setIsLoading(true)

    // Create empty bot message for streaming
    const botMessageId = Date.now()
    streamingMessageId.current = botMessageId
    setMessages((prev) => [
      ...prev,
      { id: botMessageId, role: 'bot', text: '', timestamp: new Date() },
    ])

    let fullResponse = ''

    await sendChatMessageStream(
      question,
      // onChunk - append each chunk to the message
      (chunk) => {
        fullResponse += chunk
        updateMessage(botMessageId, fullResponse)
      },
      // onDone - add sources if available
      (sources) => {
        if (sources && sources.length > 0) {
          fullResponse += `\n\n📚 Sources: ${sources.join(', ')}`
          updateMessage(botMessageId, fullResponse)
        }
        setIsLoading(false)
        streamingMessageId.current = null
      },
      // onError
      (err) => {
        console.error('Chat error:', err)
        setError(err.message || 'Failed to get response')
        updateMessage(botMessageId, 'The connection to the Akasha is disrupted. Please try again.')
        setIsLoading(false)
        streamingMessageId.current = null
      }
    )
  }, [addMessage, updateMessage])

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
