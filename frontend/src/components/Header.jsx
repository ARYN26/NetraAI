import { motion } from 'framer-motion'
import NetraIcon from './NetraIcon'

/**
 * Header component with breathing glow animation
 */
export default function Header() {
  return (
    <header className="px-6 py-6 border-b border-void-light">
      <div className="flex items-center justify-center gap-4">
        {/* Netra Icon with breathing glow */}
        <NetraIcon size={44} />

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="font-mystical text-3xl tracking-[0.3em] text-divine-gold"
        >
          NETRA
        </motion.h1>
      </div>
    </header>
  )
}
