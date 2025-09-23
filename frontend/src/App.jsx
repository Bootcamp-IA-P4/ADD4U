import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { AppStateProvider } from './contexts/AppStateContext'
import MainApp from './pages/MainApp'
import Login from './pages/Login'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <AppStateProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <ProtectedRoute>
              <MainApp />
            </ProtectedRoute>
          } />
        </Routes>
      </AppStateProvider>
    </AuthProvider>
  )
}

export default App
