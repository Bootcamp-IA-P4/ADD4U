import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
        <div className="text-center">
          <div className="h-10 w-10 rounded-md flex items-center justify-center mx-auto mb-4" style={{background: 'var(--cm-red)'}}>
            <span className="h-2 w-2 rounded-full bg-white pulse"></span>
          </div>
          <p className="text-muted">Cargando...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
