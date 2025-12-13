import { useState } from 'react'

/**
 * Input area for chat submission (matches template)
 */
export default function InputArea({ onSend, onStop, isLoading }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    onSend(input)
    setInput('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <footer className="flex-shrink-0 p-4 md:px-10 py-5 bg-background-dark border-t border-solid border-white/10">
      <form onSubmit={handleSubmit} className="relative max-w-3xl mx-auto">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Netra..."
          disabled={isLoading}
          className="w-full h-12 px-4 pr-12 rounded-lg bg-white/5 border border-white/10 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-shadow disabled:opacity-50"
        />
        <button
          type={isLoading ? "button" : "submit"}
          onClick={isLoading ? onStop : undefined}
          disabled={!isLoading && !input.trim()}
          className="absolute inset-y-0 right-0 flex items-center justify-center w-12 text-gray-400 hover:text-primary transition-colors disabled:opacity-50"
        >
          {isLoading ? (
            <span className="material-symbols-outlined text-red-400 hover:text-red-300">stop_circle</span>
          ) : (
            <span className="material-symbols-outlined">send</span>
          )}
        </button>
      </form>
    </footer>
  )
}
