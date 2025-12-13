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
        {/* Empty state */}
        {messages.length === 0 && !isLoading && (
          <div className="flex items-start gap-4 max-w-2xl">
            <div className="flex-shrink-0 size-8 rounded-full flex items-center justify-center text-primary bg-primary/20">
              <span
                className="material-symbols-outlined text-xl"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                visibility
              </span>
            </div>
            <div className="bg-white/5 rounded-lg rounded-tl-none p-4 w-full">
              <p className="text-gray-300">
                Greetings. I am Netra. How may I illuminate your path today? Ask me about the ancient
                wisdom of tantra and meditation.
              </p>
            </div>
          </div>
        )}

        {/* Messages */}
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}

        {/* Loading indicator - only show if no streaming content yet */}
        {isLoading && messages.length > 0 && !messages[messages.length - 1]?.text && (
          <div className="flex items-start gap-4 max-w-2xl">
            <div className="flex-shrink-0 size-8 rounded-full flex items-center justify-center text-primary bg-primary/20">
              <span
                className="material-symbols-outlined text-xl"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                visibility
              </span>
            </div>
            <div className="bg-white/5 rounded-lg rounded-tl-none p-4">
              <div className="flex items-center gap-1">
                <span className="loading-dot w-2 h-2 bg-primary rounded-full" />
                <span className="loading-dot w-2 h-2 bg-primary rounded-full" />
                <span className="loading-dot w-2 h-2 bg-primary rounded-full" />
              </div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={bottomRef} />
      </div>
    </main>
  )
}
