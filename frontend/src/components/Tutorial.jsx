import { useState, useEffect } from 'react'

const TUTORIAL_STORAGE_KEY = 'netra-tutorial-seen'

/**
 * Tutorial Modal - First-time user onboarding
 */
export default function Tutorial() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    // Check if user has seen the tutorial
    const hasSeenTutorial = localStorage.getItem(TUTORIAL_STORAGE_KEY)
    if (!hasSeenTutorial) {
      setIsVisible(true)
    }
  }, [])

  const handleDismiss = () => {
    localStorage.setItem(TUTORIAL_STORAGE_KEY, 'true')
    setIsVisible(false)
  }

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-background-dark border border-white/20 rounded-xl max-w-lg w-full mx-4 shadow-2xl shadow-primary/20 overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-white/10 text-center">
          <div className="flex justify-center mb-4">
            <img src="/logo.png" alt="Netra Eye" className="w-16 h-16 object-contain" />
          </div>
          <h2 className="text-2xl font-bold text-white">
            Welcome to Netra
          </h2>
          <p className="text-gray-400 mt-2">The Eye of Tantric Wisdom</p>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Purpose */}
          <div className="flex gap-4">
            <div className="flex-shrink-0 size-10 rounded-full bg-primary/20 flex items-center justify-center">
              <span className="material-symbols-outlined text-primary">temple_hindu</span>
            </div>
            <div>
              <h3 className="text-white font-medium mb-1">Spiritual Purposes Only</h3>
              <p className="text-gray-400 text-sm">
                Netra is designed exclusively for spiritual and tantric knowledge. It sources wisdom from authentic scriptures.
              </p>
            </div>
          </div>

          {/* What it can answer */}
          <div className="flex gap-4">
            <div className="flex-shrink-0 size-10 rounded-full bg-primary/20 flex items-center justify-center">
              <span className="material-symbols-outlined text-primary">self_improvement</span>
            </div>
            <div>
              <h3 className="text-white font-medium mb-1">What You Can Ask</h3>
              <p className="text-gray-400 text-sm">
                Mantras and their meanings, meditation techniques, yoga practices, tantric rituals,
                chakras, kundalini, and scriptural wisdom from Vedas, Upanishads, and Tantras.
              </p>
            </div>
          </div>

          {/* Warning */}
          <div className="flex gap-4">
            <div className="flex-shrink-0 size-10 rounded-full bg-amber-500/20 flex items-center justify-center">
              <span className="material-symbols-outlined text-amber-400">warning</span>
            </div>
            <div>
              <h3 className="text-amber-400 font-medium mb-1">Important Disclaimer</h3>
              <p className="text-gray-400 text-sm">
                This tool is for educational purposes only. Please consult a qualified guru before
                practicing any mantras or sadhana. Do not rely solely on this software for spiritual guidance.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-white/10">
          <button
            onClick={handleDismiss}
            className="w-full py-3 px-6 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 transition-all border border-purple-400/50 shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_30px_rgba(147,51,234,0.5)]"
          >
            Got it, let's begin
          </button>
        </div>
      </div>
    </div>
  )
}
