/**
 * Sidebar - Conversation history panel with collapse toggle
 */
export default function Sidebar({
  conversations = [],
  activeId,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  onClearHistory,
  isCollapsed,
  onToggleCollapse,
}) {
  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <aside className={`${isCollapsed ? 'w-16' : 'w-64'} flex-shrink-0 bg-black/20 border-r border-white/10 flex flex-col transition-all duration-300`}>
      {/* Header */}
      <div className="p-4 border-b border-white/10 flex items-center justify-between">
        <div className={`flex items-center gap-3 ${isCollapsed ? 'justify-center w-full' : ''}`}>
          <img src="/logo.png" alt="Netra Eye" className="w-12 h-12 object-contain" />
          {!isCollapsed && <h2 className="text-lg font-bold text-white">Netra</h2>}
        </div>
        {!isCollapsed && (
          <button
            onClick={onNewChat}
            className="p-1 rounded-md text-gray-400 hover:bg-white/10 hover:text-white transition-colors"
          >
            <span className="material-symbols-outlined text-xl">add</span>
          </button>
        )}
      </div>

      {/* Toggle Button */}
      <button
        onClick={onToggleCollapse}
        className="p-2 mx-2 mt-2 rounded-md text-gray-400 hover:bg-white/10 hover:text-white transition-colors flex items-center justify-center"
        title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        <span className="material-symbols-outlined text-xl">
          {isCollapsed ? 'chevron_right' : 'chevron_left'}
        </span>
      </button>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto p-2">
        {isCollapsed ? (
          <div className="flex flex-col gap-2 items-center">
            {/* New chat button when collapsed */}
            <button
              onClick={onNewChat}
              className="p-2 rounded-md text-gray-400 hover:bg-white/10 hover:text-white transition-colors"
              title="New chat"
            >
              <span className="material-symbols-outlined text-xl">add</span>
            </button>
            {/* Show chat icons for conversations when collapsed */}
            {conversations.slice(0, 5).map((conv) => (
              <button
                key={conv.id}
                onClick={() => onSelectChat(conv.id)}
                className={`p-2 rounded-md transition-colors ${
                  activeId === conv.id
                    ? 'text-white bg-primary/30'
                    : 'text-gray-400 hover:bg-white/10 hover:text-white'
                }`}
                title={conv.title}
              >
                <span className="material-symbols-outlined text-lg">chat_bubble</span>
              </button>
            ))}
          </div>
        ) : (
          <nav className="flex flex-col gap-1">
            {conversations.length === 0 && (
              <p className="text-gray-500 text-sm text-center py-8 px-4">
                No conversations yet.
                <br />
                Start a new chat to begin.
              </p>
            )}
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => onSelectChat(conv.id)}
                className={`group flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors text-left w-full ${
                  activeId === conv.id
                    ? 'text-white bg-primary/30'
                    : 'text-gray-300 hover:bg-white/10'
                }`}
              >
                <span className="material-symbols-outlined text-lg">chat_bubble</span>
                <span className="flex-1 truncate">{conv.title}</span>
                {activeId !== conv.id && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onDeleteChat(conv.id)
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 rounded transition-opacity"
                  >
                    <span className="material-symbols-outlined text-sm text-red-400">delete</span>
                  </button>
                )}
              </button>
            ))}
          </nav>
        )}
      </div>

      {/* Footer */}
      <div className={`p-4 border-t border-white/10 ${isCollapsed ? 'flex flex-col items-center gap-2' : 'space-y-1'}`}>
        {!isCollapsed && conversations.length > 0 && (
          <button
            onClick={() => {
              if (window.confirm('Clear all conversation history?')) {
                onClearHistory()
              }
            }}
            className="flex items-center gap-3 px-3 py-2 text-sm font-medium text-gray-400 rounded-md hover:bg-red-500/10 hover:text-red-400 transition-colors w-full"
          >
            <span className="material-symbols-outlined text-lg">delete_sweep</span>
            <span>Clear History</span>
          </button>
        )}
        {isCollapsed ? (
          <button
            className="p-2 rounded-md text-gray-400 hover:bg-white/10 hover:text-white transition-colors"
            title="Settings"
          >
            <span className="material-symbols-outlined text-lg">settings</span>
          </button>
        ) : (
          <a
            className="flex items-center gap-3 px-3 py-2 text-sm font-medium text-gray-300 rounded-md hover:bg-white/10 transition-colors"
            href="#"
          >
            <span className="material-symbols-outlined text-lg">settings</span>
            <span>Settings</span>
          </a>
        )}
      </div>
    </aside>
  )
}
