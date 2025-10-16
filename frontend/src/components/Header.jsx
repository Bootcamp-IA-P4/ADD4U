import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import ExportMenu from './ExportMenu'

const Header = () => {
  const { state, saveState, loadState } = useAppState()

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
    <header className="w-full">
      <div className="flex items-center justify-center py-1">
        <div className="flex items-center justify-between w-full max-w-6xl gap-2">
          {/* Logo y título centrados */}
          <div className="flex items-center gap-2">
            <div className="flex items-center justify-center -my-2">
              <img src="/images/icono2.png" alt="Mini-CELIA Logo" className="h-40 w-40 object-contain" />
            </div>
            <div>              
              <p className="text-sm font-medium text-brand-green">Copilot Inteligente de Licitaciones</p>
            </div>
          </div>
          
          {/* Botones de acción */}
          <div className="flex items-center gap-3">
            <button 
              onClick={handleSave} 
              className="px-4 py-2 rounded-xl border-2 cm-outline text-sm font-semibold flex items-center gap-2 hover:shadow-md transition-all duration-300"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <span className="hidden sm:inline">Guardar</span>
            </button>
            
            <button 
              onClick={handleLoad} 
              className="px-4 py-2 rounded-xl border-2 cm-outline text-sm font-semibold flex items-center gap-2 hover:shadow-md transition-all duration-300"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              <span className="hidden sm:inline">Cargar</span>
            </button>
            
            <ExportMenu />
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
