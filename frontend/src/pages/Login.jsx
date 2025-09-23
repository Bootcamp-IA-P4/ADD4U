import React, { useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Login = () => {
  const { login, isAuthenticated } = useAuth()
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await login(formData)
    } catch (err) {
      setError(err.message || 'Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Franja institucional */}
        <div className="w-full h-1.5 mb-8" style={{background: 'var(--cm-red)'}}></div>
        
        <div className="bg-white border border-gray-200 rounded-xl px-6 py-8 shadow-soft">
          <div className="text-center mb-6">
            <div className="h-12 w-12 rounded-md flex items-center justify-center mx-auto mb-4" style={{background: 'var(--cm-red)'}}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path d="M6 2h9a1 1 0 0 1 1 1v3h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a4 4 0 0 1-4-4V6a4 4 0 0 1 4-4zm10 10H8a1 1 0 1 0 0 2h8a1 1 0 1 0 0-2zm0 4H8a1 1 0 1 0 0 2h8a1 1 0 1 0 0-2zM16 6V4H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12V7h-2z"/>
              </svg>
            </div>
            <h1 className="text-2xl font-semibold tracking-tight mb-2">Mini‑CELIA</h1>
            <p className="text-sm text-muted">Chatbot de Licitaciones (PoC)</p>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="form-input"
                placeholder="Ingresa tu email"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-2">
                Contraseña
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-input"
                placeholder="Ingresa tu contraseña"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-3 rounded-lg cm-btn font-medium disabled:opacity-50"
            >
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </button>
          </form>

          <div className="mt-6 p-4 rounded-lg bg-gray-50 border border-gray-200">
            <p className="text-xs text-muted mb-2 font-medium">Cuentas de prueba:</p>
            <div className="space-y-1 text-xs text-muted">
              <div>Admin: admin@minicelia.es / admin123</div>
              <div>Usuario: user@minicelia.es / user123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
