import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useAppState } from '../contexts/AppStateContext'
import ExportMenu from './ExportMenu'

const Header = () => {
  const { user, logout, isAdmin } = useAuth()
  const { state, saveState, loadState } = useAppState()
  const [role, setRole] = useState('user')

  const handleSave = () => {
    if (saveState()) {
      showToast('Sesión guardada')
    }
  }

  const handleLoad = () => {
    if (loadState()) {
      showToast('Sesión cargada')
    } else {
      showToast('No hay sesión guardada')
    }
  }

  const showToast = (message) => {
    // Simple toast implementation
    const toast = document.createElement('div')
    toast.className = 'fixed bottom-4 right-4 bg-white border border-gray-200 text-ink px-4 py-2 rounded-lg shadow-soft z-50'
    toast.textContent = message
    document.body.appendChild(toast)
    setTimeout(() => {
      toast.style.opacity = '0'
      setTimeout(() => document.body.removeChild(toast), 300)
    }, 1600)
  }

  const getDraftCount = () => {
    return Object.keys(state.draft?.sections || {}).length
  }

  return (
    <header className="bg-white border border-gray-200 rounded-xl px-4 md:px-5 py-3 md:py-4 shadow-soft mb-5">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          {/* Icono abstracto rojo */}
          <div className="h-10 w-10 rounded-md flex items-center justify-center" style={{background: 'var(--cm-red)'}}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M6 2h9a1 1 0 0 1 1 1v3h2a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6a4 4 0 0 1-4-4V6a4 4 0 0 1 4-4zm10 10H8a1 1 0 1 0 0 2h8a1 1 0 1 0 0-2zm0 4H8a1 1 0 1 0 0 2h8a1 1 0 1 0 0-2zM16 6V4H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12V7h-2z"/>
            </svg>
          </div>
          <div>
            <h1 className="text-xl md:text-2xl font-semibold tracking-tight">Mini‑CELIA · Chatbot de Licitaciones</h1>
            <p className="text-sm text-muted">PoC: generación, validación y cumplimiento normativo</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="hidden sm:flex items-center gap-2 border border-gray-200 rounded-lg px-2 py-1 bg-white">
            <span className="text-xs text-muted">Usuario: {user?.name}</span>
            <span className={`text-xs px-2 py-0.5 rounded ${isAdmin ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}`}>
              {isAdmin ? 'Admin' : 'Usuario'}
            </span>
          </div>
          
          <button onClick={handleSave} className="px-3 py-2 rounded-lg border cm-outline text-sm">
            Guardar
          </button>
          
          <button onClick={handleLoad} className="px-3 py-2 rounded-lg border cm-outline text-sm">
            Cargar
          </button>
          
          <ExportMenu />
          
          <button onClick={logout} className="px-3 py-2 rounded-lg cm-btn text-sm font-medium">
            Salir
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
