/**
 * Individual chat message component (matches template)
 */
export default function Message({ message }) {
  const isBot = message.role === 'bot'

  return (
    <div className={`flex items-start gap-4 ${!isBot ? 'justify-end' : ''}`}>
      {/* Bot Avatar */}
      {isBot && (
        <div className="flex-shrink-0 size-8 rounded-full flex items-center justify-center text-primary bg-primary/20">
          <span
            className="material-symbols-outlined text-xl"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            visibility
          </span>
        </div>
      )}

      {/* Message Content */}
      <div
        className={`p-4 max-w-2xl ${
          isBot
            ? 'bg-white/5 rounded-lg rounded-tl-none'
            : 'bg-primary/20 rounded-lg rounded-br-none'
        }`}
      >
        <p className={`whitespace-pre-wrap ${isBot ? 'text-gray-300' : 'text-gray-200'}`}>
          {message.text}
        </p>
      </div>
    </div>
  )
}
