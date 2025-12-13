import { useRef, useEffect } from 'react'
import Message from './Message'

/**
 * Chat message container with auto-scroll (matches template)
 */
export default function ChatBox({ messages, isLoading }) {
  const bottomRef = useRef(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <main className="flex-1 overflow-y-auto relative">
      {/* Subtle cosmic background overlay - fixed to viewport */}
      <div
        className="fixed inset-0 bg-cover bg-center opacity-15 pointer-events-none z-0"
        style={{
          backgroundImage: `url("https://lh3.googleusercontent.com/aida-public/AB6AXuBmPUjtU79txjOZd-yAyZaxz7g-U-jKH6Is1T2KYaKdVdMrLhYQkLVuHGxychcl1Or4IvXUu_1jbZcPXpWX_o2VdmpjuZzCZ2XMLdZQ52Ny4rT0VXgdJ0kU7_luktvPIjWQOAivj89f1zDvBDcR09ihjICqwZUQzEbJaioHzeUQPV2hIpHV8LaDL1cCuqJqcgx29j9wYuCz7kJFCbaEQ0gbrDkFIx4TyhLL_Bmsr-s2kjB6hWsib94m23vQaF0FtXmgK60ynoDiTA")`,
          backgroundSize: '120%',
        }}
      />

      <div className="relative z-10 p-4 md:p-6 lg:p-8 space-y-8">
        {/* Empty state - subtle prompt */}
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full min-h-[300px] text-center">
            <span
              className="material-symbols-outlined text-6xl text-primary/30 mb-4"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              visibility
            </span>
            <p className="text-gray-500 text-sm">Ask Netra about tantric wisdom...</p>
          </div>
        )}

        {/* Messages */}
        {messages.map((message, index) => (
          <Message
            key={message.id}
            message={message}
            isStreaming={isLoading && index === messages.length - 1 && message.role === 'bot'}
          />
        ))}

        {/* Scroll anchor */}
        <div ref={bottomRef} />
      </div>
    </main>
  )
}
