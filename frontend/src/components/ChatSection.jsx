import React, { useState, useRef, useEffect } from 'react'
import { useAppState } from '../contexts/AppStateContext'
import apiService from '../services/apiService'

const ChatSection = () => {
  const { state, addMessage, escapeHtml } = useAppState()
  const [inputValue, setInputValue] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [backendStatus, setBackendStatus] = useState({ connected: null, checking: true })
  const chatBoxRef = useRef(null)
  const textareaRef = useRef(null)
  
  useEffect(() => {
    // Welcome message on first load
    if (state.chat.length === 0) {
      const welcomeMessage = '<div class="welcome-message">' +
        '<h3 style="color: var(--cm-red); font-weight: 600; margin-bottom: 16px; font-size: 1.25rem; display: flex; align-items: center; gap: 8px;">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">' +
        '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>' +
        '</svg>' +
        'Bienvenido a Mini-CELIA!' +
        '</h3>' +
        '<p style="margin-bottom: 16px; color: var(--ink);">Soy tu copilot inteligente para documentos de licitacion. Puedo ayudarte a generar:</p>' +
        '<ul style="margin-bottom: 16px; padding-left: 20px; color: var(--ink);">' +
        '<li style="margin-bottom: 8px;"><strong>Justificacion de la Necesidad (JN)</strong></li>' +
        '<li style="margin-bottom: 8px;"><strong>Pliego de Prescripciones Tecnicas (PPT)</strong></li>' +
        '<li style="margin-bottom: 8px;"><strong>Cuadro Economico de Costes (CEC)</strong></li>' +
        '<li style="margin-bottom: 8px;"><strong>Cuadro Resumen (CR)</strong></li>' +
        '</ul>' +
        '<p style="color: var(--cm-red); font-weight: 500;">Usa las acciones rapidas de abajo o escribeme directamente lo que necesitas</p>' +
        '</div>'
      
      addMessage('bot', welcomeMessage)
    }
  }, [])

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTo({
        top: chatBoxRef.current.scrollHeight,
        behavior: 'smooth'
      })
    }
  }, [state.chat, isThinking])

  // Health check del backend al cargar
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const health = await apiService.healthCheck()
        setBackendStatus({ 
          connected: health.success, 
          checking: false,
          message: health.status 
        })
      } catch (error) {
        setBackendStatus({ 
          connected: false, 
          checking: false,
          message: 'Backend no disponible' 
        })
      }
    }
    
    checkBackend()
  }, [])
  
  const handleQuickAction = async (action) => {
    const actionTexts = {
      'jn': 'Genera Justificacion de la Necesidad (JN)',
      'ppt': 'Genera Pliego de Prescripciones Tecnicas (PPT)', 
      'cec': 'Genera Cuadro Economico de Costes (CEC)',
      'cr': 'Genera Cuadro Resumen (CR)',
      'complete': 'Genera expediente completo (JN + PPT + CEC + CR)',
      'validate': 'Valida cumplimiento normativo'
    }
    
    const text = actionTexts[action]
    addMessage('user', text)
    setIsThinking(true)

    try {
      let result
      
      if (action === 'jn') {
        result = await apiService.generateJN(state.ctx)
      } else if (action === 'validate') {
        result = await apiService.validateCompliance(state.draft)
      } else if (action === 'complete') {
        result = await apiService.generateComplete(state.ctx)
      } else {
        result = await apiService.chatWithBot(text, state.ctx)
      }

      setIsThinking(false)
      
      if (result.success) {
        if (action === 'complete' && result.sections) {
          // Para expediente completo, mostrar todas las secciones
          Object.entries(result.sections).forEach(([key, content]) => {
            addMessage('bot', '<h4>Seccion ' + key.toUpperCase() + '</h4>' + content)
          })
        } else if (action === 'validate' && result.results) {
          // Para validación, mostrar resultados estructurados
          const complianceHTML = '<div class="compliance-results">' +
            '<h4 style="color: var(--cm-red);">Resultados de Validacion</h4>' +
            '<p><strong>Estado general:</strong> ' + result.results.overall + '</p>' +
            '<ul style="list-style: none; padding-left: 0;">' +
            '<li><strong>DNSH:</strong> ' + (result.results.dnsh?.details || 'N/A') + '</li>' +
            '<li><strong>RGPD:</strong> ' + (result.results.rgpd?.details || 'N/A') + '</li>' +
            '<li><strong>Fraccionamiento:</strong> ' + (result.results.fraccionamiento?.details || 'N/A') + '</li>' +
            '</ul>' +
            '</div>'
          addMessage('bot', complianceHTML)
        } else {
          addMessage('bot', result.content)
        }
        
        if (!result.success && result.error) {
          console.warn('API returned success=false:', result.error)
        }
      } else {
        // Mostrar contenido de fallback con indicador de error
        addMessage('bot', result.content)
        if (result.error) {
          console.error('API Error:', result.error)
        }
      }
    } catch (error) {
      setIsThinking(false)
      console.error('Error in handleQuickAction:', error)
      addMessage('bot', 'Error: ' + error.message + '. Mostrando respuesta de fallback.')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const text = inputValue.trim()
    if (!text) return

    addMessage('user', escapeHtml(text))
    setInputValue('')
    setIsThinking(true)

    try {
      // Usar la API real para procesar el mensaje
      const result = await apiService.chatWithBot(text, state.ctx)
      
      setIsThinking(false)
      
      if (result.success) {
        addMessage('bot', result.content)
      } else {
        // Mostrar respuesta de fallback
        addMessage('bot', result.content)
        if (result.error) {
          console.error('Chat API Error:', result.error)
        }
      }
    } catch (error) {
      setIsThinking(false)
      console.error('Error in handleSubmit:', error)
      
      // Fallback a respuesta local
      addMessage('bot', 'Error de conexion: ' + error.message + '. Usando respuesta local...')
      setTimeout(() => {
        botReply(text)
      }, 500)
    }
  }

  const botReply = (text) => {
    const lowerText = text.toLowerCase()
    
    // Check for missing context
    const missing = []
    if (!state.ctx.proceso) missing.push('proceso')
    if (!state.ctx.entidad) missing.push('entidad')
    if (!state.ctx.fecha) missing.push('fecha limite')
    
    if (missing.length > 0) {
      addMessage('bot', 'Me falta: ' + missing.join(', ') + '. Completalo arriba para afinar la redaccion.')
      return
    }

    // Simple bot responses based on keywords
    if (lowerText.includes('generar jn') || lowerText.includes('justificacion')) {
      addMessage('bot', 'Seccion Justificacion de la Necesidad generada.')
    } else if (lowerText.includes('generar ppt') || lowerText.includes('pliego')) {
      addMessage('bot', 'Seccion Pliego Tecnico generada.')
    } else if (lowerText.includes('generar cec') || lowerText.includes('presupuesto')) {
      addMessage('bot', 'Seccion Presupuesto (CEC) generada.')
    } else if (lowerText.includes('generar cr') || lowerText.includes('cuadro resumen')) {
      addMessage('bot', 'Seccion Cuadro Resumen (CR) generada.')
    } else if (lowerText.includes('cumplimiento')) {
      addMessage('bot', 'Evaluando cumplimiento normativo: DNSH/PRTR, RGPD y no fraccionamiento.')
    } else if (lowerText.includes('coherencia')) {
      addMessage('bot', 'Validando coherencia inter-documental: lotes, pesos y plazos.')
    } else {
      addMessage('bot', 'Quieres que orqueste el flujo completo ahora (JN + PPT + CEC + CR) o generamos una seccion concreta?')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const renderMessage = (message) => {
    if (message.role === 'bot') {
      return (
        <div key={message.id} className="flex items-start gap-4 animate-fade-in">
          <div className="h-10 w-10 rounded-full flex items-center justify-center bot-avatar flex-shrink-0">
            <span className="h-2.5 w-2.5 rounded-full bg-white pulse"></span>
          </div>
          <div 
            className="max-w-[80%] md:max-w-[70%] rounded-2xl bot-bubble px-6 py-4 text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: message.content }}
          />
        </div>
      )
    } else {
      return (
        <div key={message.id} className="flex items-start gap-4 justify-end animate-fade-in">
          <div 
            className="max-w-[80%] md:max-w-[70%] rounded-2xl user-bubble px-6 py-4 text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: message.content }}
          />
          <div className="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
            <svg className="w-5 h-5 text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
        </div>
      )
    }
  }

  const getStatusClass = () => {
    if (backendStatus.checking) {
      return 'bg-yellow-50 text-yellow-700 border border-yellow-200'
    } else if (backendStatus.connected) {
      return 'bg-green-50 text-green-700 border border-green-200'
    } else {
      return 'bg-red-50 text-red-700 border border-red-200'
    }
  }

  return (
    <section className="w-full">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold flex items-center gap-2" style={{color: 'var(--cm-red)'}}>
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          Chat Inteligente
        </h2>
        <div className="flex items-center gap-3">
          <div className={'flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ' + getStatusClass()}>
            {backendStatus.checking ? (
              <>
                <svg className="w-3 h-3 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                Verificando...
              </>
            ) : backendStatus.connected ? (
              <>
                <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10"/>
                </svg>
                OpenAI Conectado
              </>
            ) : (
              <>
                <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10"/>
                </svg>
                Modo Offline
              </>
            )}
          </div>
          <div className="text-sm text-muted bg-white px-4 py-2 rounded-full border border-gray-200">
            Pregunta, propone y corrige
          </div>
        </div>
      </div>
      
      <div 
        ref={chatBoxRef}
        className="h-[60vh] overflow-y-auto scrollbar pr-2 space-y-6 mb-6"
      >
        {state.chat.map(renderMessage)}
        
        {isThinking && (
          <div className="flex items-start gap-4 animate-pulse">
            <div className="h-10 w-10 rounded-full flex items-center justify-center bot-avatar">
              <span className="h-2.5 w-2.5 rounded-full bg-white pulse"></span>
            </div>
            <div className="max-w-[80%] md:max-w-[70%] rounded-2xl bot-bubble px-6 py-4 text-sm leading-relaxed">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                </div>
                <span className="text-muted">Procesando tu consulta...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Acciones rapidas integradas */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-4">
          <h3 className="text-sm font-semibold text-muted flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            Acciones Rapidas
          </h3>
          <div className="flex-1 h-px bg-gradient-to-r from-gray-200 to-transparent"></div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button 
            onClick={() => handleQuickAction('jn')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-xl border-2 border-emerald-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
            </svg>
            Generar JN
          </button>
          <button 
            onClick={() => handleQuickAction('ppt')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-blue-50 hover:bg-blue-100 text-blue-800 rounded-xl border-2 border-blue-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="12" y1="18" x2="12" y2="12"/>
              <line x1="9" y1="15" x2="15" y2="15"/>
            </svg>
            Generar PPT
          </button>
          <button 
            onClick={() => handleQuickAction('cec')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-xl border-2 border-amber-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
            Generar CEC
          </button>
          <button 
            onClick={() => handleQuickAction('cr')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-purple-50 hover:bg-purple-100 text-purple-800 rounded-xl border-2 border-purple-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <path d="M9 9h6v6H9z"/>
            </svg>
            Generar CR
          </button>
          <button 
            onClick={() => handleQuickAction('complete')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-red-50 hover:bg-red-100 text-red-800 rounded-xl border-2 border-red-200 disabled:opacity-50 font-medium col-span-2 md:col-span-1"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            Expediente completo
          </button>
          <button 
            onClick={() => handleQuickAction('validate')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-gray-50 hover:bg-gray-100 text-gray-800 rounded-xl border-2 border-gray-200 disabled:opacity-50 font-medium col-span-2 md:col-span-2"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9,11 12,14 22,4"/>
              <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9s4.03-9 9-9c1.11 0 2.16.2 3.14.57"/>
            </svg>
            Validar cumplimiento normativo
          </button>
        </div>
      </div>

      {/* Input de chat mejorado */}
      <div className="bg-white rounded-2xl border-2 border-gray-100 p-4 shadow-lg">
        <form onSubmit={handleSubmit} className="flex items-end gap-4">
          <div className="flex-1">
            <label htmlFor="userInput" className="sr-only">Escribe tu mensaje</label>
            <textarea
              ref={textareaRef}
              id="userInput"
              rows="2"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              className="form-textarea border-0 bg-gray-50 focus:bg-white"
              placeholder="Escribe tu consulta aqui o usa las acciones rapidas de arriba..."
            />
          </div>
          <button 
            type="submit"
            disabled={!inputValue.trim() || isThinking}
            className="px-6 py-3 rounded-xl cm-btn font-semibold disabled:opacity-50 flex items-center gap-2"
          >
            {isThinking ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Procesando...
              </>
            ) : (
              <>
                <span>Enviar</span>
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22,2 15,22 11,13 2,9 22,2"/>
                </svg>
              </>
            )}
          </button>
        </form>
      </div>
    </section>
  )
}

export default ChatSection
