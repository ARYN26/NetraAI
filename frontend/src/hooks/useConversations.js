import { useState, useEffect, useCallback } from 'react'

const STORAGE_KEY = 'netra_conversations'

/**
 * Generate a unique ID for conversations
 */
const generateId = () => {
  return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Generate a title from the first message
 */
const generateTitle = (message, maxLength = 30) => {
  if (!message) return 'New Conversation'
  const cleaned = message.trim().replace(/\s+/g, ' ')
  if (cleaned.length <= maxLength) return cleaned
  return cleaned.substring(0, maxLength) + '...'
}

/**
 * Hook for managing conversation history in localStorage
 */
export function useConversations() {
  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [isLoaded, setIsLoaded] = useState(false)

  // Load conversations from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const data = JSON.parse(stored)
        setConversations(data.conversations || [])
        setActiveId(data.activeConversationId || null)
      }
    } catch (error) {
      console.error('Failed to load conversations:', error)
    }
    setIsLoaded(true)
  }, [])

  // Save to localStorage whenever state changes
  useEffect(() => {
    if (!isLoaded) return

    try {
      const data = {
        conversations,
        activeConversationId: activeId,
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    } catch (error) {
      console.error('Failed to save conversations:', error)
    }
  }, [conversations, activeId, isLoaded])

  // Get the active conversation
  const activeConversation = conversations.find(c => c.id === activeId) || null

  // Create a new conversation
  const createConversation = useCallback(() => {
    const newConv = {
      id: generateId(),
      title: 'New Conversation',
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }

    setConversations(prev => [newConv, ...prev])
    setActiveId(newConv.id)
    return newConv
  }, [])

  // Select a conversation
  const selectConversation = useCallback((id) => {
    setActiveId(id)
  }, [])

  // Add a message to the active conversation
  const addMessage = useCallback((role, content) => {
    if (!activeId) return

    const newMessage = {
      role,
      content,
      timestamp: new Date().toISOString(),
    }

    setConversations(prev => prev.map(conv => {
      if (conv.id !== activeId) return conv

      const updatedMessages = [...conv.messages, newMessage]

      // Update title from first user message if still default
      let title = conv.title
      if (conv.messages.length === 0 && role === 'user') {
        title = generateTitle(content)
      }

      return {
        ...conv,
        messages: updatedMessages,
        title,
        updatedAt: new Date().toISOString(),
      }
    }))
  }, [activeId])

  // Delete a conversation
  const deleteConversation = useCallback((id) => {
    setConversations(prev => prev.filter(c => c.id !== id))

    // If deleting active conversation, clear active
    if (activeId === id) {
      setActiveId(null)
    }
  }, [activeId])

  // Clear all conversations
  const clearAllConversations = useCallback(() => {
    setConversations([])
    setActiveId(null)
  }, [])

  // Update messages for active conversation (for loading existing)
  const setActiveMessages = useCallback((messages) => {
    if (!activeId) return

    setConversations(prev => prev.map(conv => {
      if (conv.id !== activeId) return conv
      return {
        ...conv,
        messages,
        updatedAt: new Date().toISOString(),
      }
    }))
  }, [activeId])

  return {
    conversations,
    activeConversation,
    activeId,
    isLoaded,
    createConversation,
    selectConversation,
    addMessage,
    deleteConversation,
    clearAllConversations,
    setActiveMessages,
  }
}
