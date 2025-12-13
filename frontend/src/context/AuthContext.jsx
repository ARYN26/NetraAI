import { createContext, useContext, useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem('netra-token'))
  const [isLoading, setIsLoading] = useState(true)

  // Load user on mount if token exists
  useEffect(() => {
    if (token) {
      fetchUser()
    } else {
      setIsLoading(false)
    }
  }, [])

  const fetchUser = async (tokenOverride) => {
    const authToken = tokenOverride || token
    try {
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        // Token invalid, clear it
        localStorage.removeItem('netra-token')
        setToken(null)
        setUser(null)
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const requestOtp = async (email) => {
    const response = await fetch(`${API_URL}/auth/request-otp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to send verification code')
    }

    return await response.json()
  }

  const verifyOtp = async (email, code) => {
    const response = await fetch(`${API_URL}/auth/verify-otp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, code }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Invalid verification code')
    }

    const data = await response.json()
    localStorage.setItem('netra-token', data.access_token)
    setToken(data.access_token)

    // Fetch user info - pass token directly to avoid React state timing issue
    await fetchUser(data.access_token)

    return data
  }

  const logout = () => {
    // Clear authentication data
    localStorage.removeItem('netra-token')
    // Clear conversation history (security: don't leave data for next user)
    localStorage.removeItem('netra-conversations')
    // Clear any other app state
    localStorage.removeItem('netra-sidebar-collapsed')
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    isLoading,
    isAuthenticated: !!user,
    requestOtp,
    verifyOtp,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
