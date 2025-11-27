/**
 * NetraIcon - Third Eye in Triangle (Ajna Chakra symbol)
 * Elegant SVG with subtle breathing glow animation - Purple theme
 */
export default function NetraIcon({ size = 40 }) {
  return (
    <div
      className="netra-icon-container relative flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      {/* Soft radial glow behind the icon */}
      <div className="netra-icon-glow absolute inset-0 z-0" />

      {/* SVG Icon */}
      <svg
        className="relative z-10"
        width={size}
        height={size}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Outer Triangle */}
        <path
          d="M24 4L44 40H4L24 4Z"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />

        {/* Eye Shape */}
        <path
          d="M12 24C12 24 17 18 24 18C31 18 36 24 36 24C36 24 31 30 24 30C17 30 12 24 12 24Z"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />

        {/* Pupil/Iris */}
        <circle
          cx="24"
          cy="24"
          r="3"
          fill="currentColor"
        />

        {/* Inner dot (bindu) */}
        <circle
          cx="24"
          cy="24"
          r="1"
          fill="#0a0a1a"
        />
      </svg>
    </div>
  )
}
