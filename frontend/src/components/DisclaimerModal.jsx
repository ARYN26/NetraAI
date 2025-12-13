/**
 * Disclaimer Modal - Shows warning at the start of each new conversation
 */
export default function DisclaimerModal({ isOpen, onAccept }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-background-dark border border-white/20 rounded-xl max-w-md w-full mx-4 shadow-2xl shadow-primary/20">
        {/* Header with icon */}
        <div className="p-6 text-center border-b border-white/10">
          <div className="flex justify-center mb-4">
            <div className="size-16 rounded-full bg-amber-500/20 flex items-center justify-center">
              <span className="material-symbols-outlined text-amber-400 text-3xl">warning</span>
            </div>
          </div>
          <h2 className="text-xl font-bold text-white">Important Disclaimer</h2>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <p className="text-gray-300 text-sm leading-relaxed">
            Netra shares tantric wisdom for <span className="text-white font-medium">educational purposes only</span>.
          </p>
          <p className="text-gray-300 text-sm leading-relaxed">
            Always consult <span className="text-white font-medium">qualified teachers</span> for spiritual practices.
            Improper practice can be harmful.
          </p>
          <p className="text-amber-400/90 text-sm leading-relaxed">
            Proceed with reverence and discernment.
          </p>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-white/10">
          <button
            onClick={onAccept}
            className="w-full py-3 px-6 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 transition-all border border-purple-400/50 shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_30px_rgba(147,51,234,0.5)]"
          >
            I Understand, Continue
          </button>
        </div>
      </div>
    </div>
  )
}
