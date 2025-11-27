import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import LandingPage from './components/LandingPage'
import ChatPage from './components/ChatPage'
import Auth from './pages/Auth'

/**
 * Landing page wrapper with navigation
 */
function LandingPageWrapper() {
  const navigate = useNavigate()
  return <LandingPage onStartChat={() => navigate('/chat')} />
}

/**
 * Chat page wrapper with navigation
 */
function ChatPageWrapper() {
  const navigate = useNavigate()
  return <ChatPage onBackToLanding={() => navigate('/')} />
}

/**
 * Main App component with routing
 */
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LandingPageWrapper />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/login" element={<Navigate to="/auth" replace />} />
          <Route path="/signup" element={<Navigate to="/auth" replace />} />
          <Route path="/chat" element={<ChatPageWrapper />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
