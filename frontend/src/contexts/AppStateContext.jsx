import React, { createContext, useContext, useState, useEffect } from 'react'
import { format, parseISO } from 'date-fns'
import { es } from 'date-fns/locale'

const AppStateContext = createContext()

export const useAppState = () => {
  const context = useContext(AppStateContext)
  if (!context) {
    throw new Error('useAppState must be used within an AppStateProvider')
  }
  return context
}

const initialState = {
  ctx: { proceso: '', entidad: '', fecha: '' },
  steps: [
    { id: 'JN', name: 'Justificación de la Necesidad', status: 'pendiente', content: '', citations: [] },
    { id: 'PPT', name: 'Pliego Técnico', status: 'pendiente', content: '', citations: [] },
    { id: 'CEC', name: 'Presupuesto (CEC)', status: 'pendiente', content: '', citations: [] },
    { id: 'CR', name: 'Cuadro Resumen (CR)', status: 'pendiente', content: '', citations: [] }
  ],
  compliance: { DNSH: false, PRTR: false, RGPD: false, Fracc: false, Missing: [] },
  coherence: { checked: false, ok: false, notes: [] },
  chat: []
}

export const AppStateProvider = ({ children }) => {
  const [state, setState] = useState(initialState)
  const [draft, setDraft] = useState({ sections: {} })
  const [showDraftModal, setShowDraftModal] = useState(false)
  const [showExportMenu, setShowExportMenu] = useState(false)

  // Utilidades
  const formatDate = (dateString) => {
    try {
      if (!dateString) return ''
      const date = typeof dateString === 'string' ? parseISO(dateString) : dateString
      return format(date, 'dd MMM yyyy', { locale: es })
    } catch {
      return dateString || ''
    }
  }

  const escapeHtml = (str) => {
    if (!str) return ''
    return str.replace(/[&<>"']/g, (match) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[match]))
  }

  const wordCount = (text) => {
    if (!text) return 0
    return (text.trim().match(/\S+/g) || []).length
  }

  // Gestión de pasos
  const getStep = (id) => state.steps.find(s => s.id === id)

  const updateStep = (id, updates) => {
    setState(prev => ({
      ...prev,
      steps: prev.steps.map(step => 
        step.id === id ? { ...step, ...updates } : step
      )
    }))
  }

  const setStepContent = (id, content, citations = []) => {
    updateStep(id, {
      content,
      citations,
      status: 'generado'
    })
  }

  // Gestión del contexto
  const updateContext = (field, value) => {
    setState(prev => ({
      ...prev,
      ctx: { ...prev.ctx, [field]: value }
    }))
  }

  // Gestión del chat
  const addMessage = (role, content) => {
    const message = {
      id: Date.now(),
      role,
      content,
      timestamp: new Date()
    }
    setState(prev => ({
      ...prev,
      chat: [...prev.chat, message]
    }))
  }

  // Gestión del borrador
  const addToDraft = (name, content) => {
    if (!content) return
    setDraft(prev => ({
      ...prev,
      sections: { ...prev.sections, [name]: content }
    }))
  }

  const updateDraftSection = (name, content) => {
    setDraft(prev => ({
      ...prev,
      sections: { ...prev.sections, [name]: content }
    }))
  }

  const removeDraftSection = (name) => {
    setDraft(prev => {
      const { [name]: removed, ...rest } = prev.sections
      return { ...prev, sections: rest }
    })
  }

  const clearDraft = () => {
    setDraft({ sections: {} })
  }

  // Cumplimiento normativo
  const updateCompliance = (compliance) => {
    setState(prev => ({ ...prev, compliance }))
  }

  // Coherencia
  const updateCoherence = (coherence) => {
    setState(prev => ({ ...prev, coherence }))
  }

  // Progreso
  const getProgress = () => {
    const total = state.steps.length
    const completed = state.steps.filter(s => s.status !== 'pendiente').length
    return Math.round((completed / total) * 100)
  }

  const getContextCompletion = () => {
    const fields = ['proceso', 'entidad', 'fecha']
    const filled = fields.filter(field => state.ctx[field]).length
    return { filled, total: fields.length }
  }

  // Guardar/Cargar estado
  const saveState = () => {
    const payload = { state, draft }
    localStorage.setItem('mini_celia_poc', JSON.stringify(payload))
    return true
  }

  const loadState = () => {
    try {
      const saved = localStorage.getItem('mini_celia_poc')
      if (!saved) return false
      
      const payload = JSON.parse(saved)
      if (payload.state) {
        setState(payload.state)
      }
      if (payload.draft) {
        setDraft(payload.draft)
      }
      return true
    } catch (error) {
      console.error('Error loading state:', error)
      return false
    }
  }

  const value = {
    // Estado
    state,
    setState,
    draft,
    setDraft,
    
    // Modales
    showDraftModal,
    setShowDraftModal,
    showExportMenu,
    setShowExportMenu,

    // Utilidades
    formatDate,
    escapeHtml,
    wordCount,

    // Pasos
    getStep,
    updateStep,
    setStepContent,

    // Contexto
    updateContext,

    // Chat
    addMessage,

    // Borrador
    addToDraft,
    updateDraftSection,
    removeDraftSection,
    clearDraft,

    // Cumplimiento y coherencia
    updateCompliance,
    updateCoherence,

    // Progreso
    getProgress,
    getContextCompletion,

    // Persistencia
    saveState,
    loadState
  }

  return (
    <AppStateContext.Provider value={value}>
      {children}
    </AppStateContext.Provider>
  )
}
