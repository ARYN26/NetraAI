import { useState, useEffect, useCallback, useRef } from 'react'
import Sidebar from './Sidebar'
import ChatBox from './ChatBox'
import InputArea from './InputArea'
import Tutorial from './Tutorial'
import { useConversations } from '../hooks/useConversations'
import { sendChatMessageStream } from '../services/api'

/**
 * ChatPage - Main chat interface with sidebar (matches template)
 */
export default function ChatPage({ onBackToLanding }) {
  const {
    conversations,
    activeConversation,
    activeId,
    isLoaded,
    createConversation,
    selectConversation,
    addMessage,
    updateLastMessage,
    deleteConversation,
    clearAllConversations,
  } = useConversations()

  // Ref for abort controller (allows canceling streaming requests)
  const abortControllerRef = useRef(null)

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => {
    const saved = localStorage.getItem('netra-sidebar-collapsed')
    return saved === 'true'
  })

  // Save sidebar state to localStorage
  const handleToggleSidebar = useCallback(() => {
    setIsSidebarCollapsed(prev => {
      const newState = !prev
      localStorage.setItem('netra-sidebar-collapsed', String(newState))
      return newState
    })
  }, [])

  // Auto-create a conversation if none exists on mount
  useEffect(() => {
    if (isLoaded && conversations.length === 0) {
      createConversation()
    }
  }, [isLoaded, conversations.length, createConversation])

  // Get current messages
  const messages = activeConversation?.messages || []

  // Transform messages for ChatBox
  const chatMessages = messages.map((msg, index) => ({
    id: `${activeId}_${index}`,
    role: msg.role === 'user' ? 'user' : 'bot',
    text: msg.content,
    timestamp: msg.timestamp,
  }))

  // Handle sending a message with streaming
  const handleSend = useCallback(async (input) => {
    if (!input.trim() || isLoading) return

    // Cancel any existing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    abortControllerRef.current = new AbortController()

    const isFirstMessage = messages.length === 0

    // Add one-time welcome/warning on first message
    if (isFirstMessage) {
      addMessage('assistant',
        'Namaste. I share tantric wisdom for educational purposes only. ' +
        'Always consult qualified teachers for spiritual practices. ' +
        'Improper practice can be harmful. Proceed with reverence.'
      )
    }

    addMessage('user', input)
    setIsLoading(true)
    setError(null)

    // Add empty assistant message for streaming
    addMessage('assistant', '')

    let fullResponse = ''

    await sendChatMessageStream(
      input,
      // onChunk - append each chunk
      (chunk) => {
        fullResponse += chunk
        updateLastMessage(fullResponse)
      },
      // onDone - add sources if available
      (sources) => {
        if (sources && sources.length > 0) {
          fullResponse += `\n\n📚 Sources: ${sources.join(', ')}`
          updateLastMessage(fullResponse)
        }
        setIsLoading(false)
        abortControllerRef.current = null
      },
      // onError
      (err) => {
        console.error('Chat error:', err)
        setError(err.message || 'Failed to get response')
        updateLastMessage('The connection to the Akasha is disrupted. Please try again.')
        setIsLoading(false)
        abortControllerRef.current = null
      },
      abortControllerRef.current.signal
    )
  }, [addMessage, updateLastMessage, isLoading, messages.length])

  // Handle stopping the current request
  const handleStop = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    setIsLoading(false)
  }, [])

  // Handle new chat
  const handleNewChat = useCallback(() => {
    createConversation()
  }, [createConversation])

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-dark">
        <div className="flex items-center gap-2">
          <span className="loading-dot w-2 h-2 bg-primary rounded-full" />
          <span className="loading-dot w-2 h-2 bg-primary rounded-full" />
          <span className="loading-dot w-2 h-2 bg-primary rounded-full" />
        </div>
      </div>
    )
  }

  return (
    <div className="relative flex h-screen w-full flex-row bg-background-dark text-gray-200 overflow-hidden">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onNewChat={handleNewChat}
        onSelectChat={selectConversation}
        onDeleteChat={deleteConversation}
        onClearHistory={clearAllConversations}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={handleToggleSidebar}
      />

      {/* Main Chat Area */}
      <div className="layout-container flex h-full grow flex-col">
        {/* Header */}
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-white/10 px-4 md:px-10 py-3 flex-shrink-0">
          <div className="flex items-center gap-4 text-white">
            <h2 className="text-lg font-bold leading-tight tracking-[-0.015em]">
              {activeConversation?.title || 'New Conversation'}
            </h2>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToLanding}
              className="text-gray-400 hover:text-white text-sm transition-colors"
            >
              Home
            </button>
            <button className="p-2 rounded-full hover:bg-white/10 transition-colors">
              <span className="material-symbols-outlined">more_horiz</span>
            </button>
          </div>
        </header>

        {/* Error Banner */}
        {error && (
          <div className="bg-red-900/30 border-b border-red-800 px-6 py-3 flex-shrink-0">
            <div className="flex justify-between items-center">
              <span className="text-red-300 text-sm">{error}</span>
              <button
                onClick={() => setError(null)}
                className="text-red-400 hover:text-red-200 text-sm"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* Chat Messages Area */}
        <ChatBox messages={chatMessages} isLoading={isLoading} />

        {/* Input Area */}
        <InputArea onSend={handleSend} onStop={handleStop} isLoading={isLoading} />
      </div>

      {/* Tutorial Modal for first-time users */}
      <Tutorial />
    </div>
  )
}
