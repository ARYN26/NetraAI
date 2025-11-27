import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Auth() {
  const [email, setEmail] = useState('')
  const [code, setCode] = useState('')
  const [step, setStep] = useState('email') // 'email' or 'code'
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { requestOtp, verifyOtp } = useAuth()
  const navigate = useNavigate()

  const handleRequestOtp = async (e) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await requestOtp(email)
      setStep('code')
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleVerifyOtp = async (e) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await verifyOtp(email, code)
      navigate('/chat')
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleResendCode = async () => {
    setError('')
    setIsLoading(true)
    setCode('')

    try {
      await requestOtp(email)
      setError('') // Clear any previous error
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleBackToEmail = () => {
    setStep('email')
    setCode('')
    setError('')
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background-dark px-4 py-8">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-3">
            <img src="/logo.png" alt="Netra Eye" className="w-16 h-16 object-contain" />
            <h1 className="text-3xl font-bold text-white">
              Netra
            </h1>
          </Link>
          <p className="text-gray-400 mt-2">
            {step === 'email'
              ? 'Enter your email to continue'
              : 'Enter the verification code'}
          </p>
        </div>

        {/* Form */}
        <div className="bg-black/30 border border-white/10 rounded-xl p-8 space-y-5">
          {error && (
            <div className="bg-red-900/30 border border-red-800 rounded-lg px-4 py-3 text-red-300 text-sm">
              {error}
            </div>
          )}

          {step === 'email' ? (
            <form onSubmit={handleRequestOtp} className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                  placeholder="Enter your email"
                  required
                  autoFocus
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 px-6 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 transition-all border border-purple-400/50 shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_30px_rgba(147,51,234,0.5)] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending code...' : 'Send Verification Code'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOtp} className="space-y-5">
              <div className="text-center mb-4">
                <p className="text-gray-400 text-sm">
                  We sent a code to <span className="text-white font-medium">{email}</span>
                </p>
              </div>

              <div>
                <label htmlFor="code" className="block text-sm font-medium text-gray-300 mb-2">
                  Verification Code
                </label>
                <input
                  type="text"
                  id="code"
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  className="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-lg text-white text-center text-2xl tracking-[0.5em] placeholder-gray-500 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors font-mono"
                  placeholder="000000"
                  maxLength={6}
                  required
                  autoFocus
                />
              </div>

              <button
                type="submit"
                disabled={isLoading || code.length !== 6}
                className="w-full py-3 px-6 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 transition-all border border-purple-400/50 shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_30px_rgba(147,51,234,0.5)] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Verifying...' : 'Verify & Continue'}
              </button>

              <div className="flex items-center justify-between pt-2">
                <button
                  type="button"
                  onClick={handleBackToEmail}
                  className="text-sm text-gray-400 hover:text-white transition-colors"
                >
                  Change email
                </button>
                <button
                  type="button"
                  onClick={handleResendCode}
                  disabled={isLoading}
                  className="text-sm text-primary hover:text-primary/80 transition-colors disabled:opacity-50"
                >
                  Resend code
                </button>
              </div>
            </form>
          )}

          <div className="pt-4 border-t border-white/10">
            <p className="text-center text-gray-500 text-xs">
              By continuing, you agree to Netra's Terms of Service
            </p>
          </div>
        </div>

        <p className="text-center text-gray-500 text-sm mt-6">
          <Link to="/" className="text-primary hover:text-primary/80 transition-colors">
            Back to home
          </Link>
        </p>
      </div>
    </div>
  )
}
