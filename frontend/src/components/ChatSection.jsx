import React, { useState, useRef, useEffect } from 'react'
import { useAppState } from '../contexts/AppStateContext'
import apiService from '../services/apiService'

const ChatSection = () => {
  const { state, addMessage, escapeHtml } = useAppState()
  const [inputValue, setInputValue] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [backendStatus, setBackendStatus] = useState({ connected: null, checking: true })
  const [conversationState, setConversationState] = useState({
    waitingFor: null, // 'expediente_id' | 'user_description' | null
    selectedJNType: null,
    expediente_id: null,
    user_text: null
  })
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
  const getJNTypeDescription = (jnType) => {
    const descriptions = {
      'jn_obras': 'Obras públicas y construcción',
      'jn_servicios': 'Servicios generales',
      'jn_suministros': 'Suministros y materiales',
      'jn_mantenimiento': 'Mantenimiento y conservación',
      'jn_tecnologia': 'Tecnología y sistemas informáticos',
      'jn_formacion': 'Formación y capacitación'
    }
    return descriptions[jnType] || 'Justificación de Necesidad'
  }

  const generateJNFromConversation = async (expedienteId, userText, selectedType) => {
    try {
      console.log('🔍 Generando JN con datos:', { expedienteId, userText, selectedType })
      
      const formData = {
        expediente_id: expedienteId,
        seccion: "JN.1", 
        user_text: userText,
        structured_llm_choice: "openai",
        narrative_llm_choice: "groq"
      }

      console.log('📤 Enviando datos a la API:', formData)
      
      // Validar que tenemos todos los datos necesarios
      if (!formData.expediente_id || !formData.user_text) {
        throw new Error(`Faltan datos requeridos: expediente_id=${formData.expediente_id}, user_text=${formData.user_text}`)
      }
      
      const result = await apiService.generateJN(formData)
      
      setIsThinking(false)
      
      if (result.success) {
        addMessage('bot', result.content)
      } else {
        addMessage('bot', result.content || 'Error al generar la JN. Por favor, inténtalo de nuevo.')
        if (result.error) {
          console.error('JN Generation Error:', result.error)
        }
      }    } catch (error) {
      setIsThinking(false)
      console.error('Error generating JN:', error)
      addMessage('bot', `❌ <strong>Error al conectar con la API:</strong> ${error.message}<br><br>Verifica que el backend esté funcionando en <code>http://localhost:8000</code> y que tengas las variables de entorno configuradas.`)
    }

    // Reset conversation state
    setConversationState({
      waitingFor: null,
      selectedJNType: null,
      expediente_id: null,
      user_text: null
    })
  }
  const handleQuickAction = (action) => {
    if (action.startsWith('jn_')) {
      const jnDescription = getJNTypeDescription(action)
      
      // Set conversation state and ask for expediente ID
      setConversationState({
        waitingFor: 'expediente_id',
        selectedJNType: action,
        expediente_id: null,
        user_text: null
      });      const message = `<strong>📋 Iniciando Justificación de Necesidad: ${jnDescription}</strong><br><br>` +
        `Para generar tu JN necesito estos datos:<br>` +
        `• <strong>ID del expediente</strong> (usuario define)<br>` +
        `• <strong>Descripción detallada</strong> (usuario define)<br>` +
        `• <strong>Sección:</strong> JN.1 (autocompletado como inicio)<br><br>` +
        `<strong>Empezamos:</strong><br>` +
        `¿Cómo quieres llamar a tu expediente? Dame el ID o título.<br><br>` +
        `<em>Ejemplos: PTX_001, OBR_MERCADILLOS, SRV_LIMPIEZA, TEC_SOFTWARE, etc.</em>`

      addMessage('bot', message)
    }
  }
  const handleSubmit = async (e) => {
    e.preventDefault()
    const text = inputValue.trim()
    if (!text) return

    addMessage('user', escapeHtml(text))
    setInputValue('')

    // Handle conversation flow for JN generation
    if (conversationState.waitingFor === 'expediente_id') {
      // User provided expediente ID
      const expedienteId = text.toUpperCase().replace(/\s+/g, '_')
      
      setConversationState(prev => ({
        ...prev,
        waitingFor: 'user_description',
        expediente_id: expedienteId
      }));

      const message = `<strong>✓ Expediente: ${expedienteId}</strong><br><br>` +
        `Perfecto! Ahora necesito que me expliques detalladamente:<br><br>` +
        `• <strong>¿Qué actividades o servicios incluye?</strong><br>` +
        `• <strong>¿Dónde se llevará a cabo?</strong><br>` +
        `• <strong>¿Por qué es necesario este expediente?</strong><br>` +
        `• <strong>¿Cuál es el objetivo principal?</strong><br><br>` +
        `Cuanto más detalle me proporciones, mejor será la justificación que genere para ti.`

      addMessage('bot', message)
      return
    }

    if (conversationState.waitingFor === 'user_description') {
      // User provided description, now generate JN
      setConversationState(prev => ({
        ...prev,
        waitingFor: null,
        user_text: text
      }));

      const confirmMessage = `<strong>✅ Información completa recibida</strong><br><br>` +
        `<strong>Expediente:</strong> ${conversationState.expediente_id}<br>` +
        `<strong>Tipo:</strong> ${getJNTypeDescription(conversationState.selectedJNType)}<br>` +
        `<strong>Descripción:</strong> ${text.substring(0, 100)}${text.length > 100 ? '...' : ''}<br><br>` +
        `🔄 <strong>Generando tu Justificación de la Necesidad...</strong>`

      addMessage('bot', confirmMessage)
      
      // Update conversation state and immediately start generation
      setConversationState(prev => ({
        ...prev,
        waitingFor: null,
        user_text: text
      }))
        // Start thinking animation immediately
      setIsThinking(true)

      // Generate JN with complete data - pasar datos directamente para evitar problemas de estado
      setTimeout(() => {
        generateJNFromConversation(conversationState.expediente_id, text, conversationState.selectedJNType)
      }, 800)
      
      return
    }

    // Regular chat flow
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

  const getPlaceholder = () => {
    if (conversationState.waitingFor === 'expediente_id') {
      return 'Escribe el ID o título del expediente (ej: PTX_001, OBR_MERCADILLOS)...'
    } else if (conversationState.waitingFor === 'user_description') {
      return 'Describe detalladamente las actividades, objetivos y justificación...'
    } else {
      return 'Escribe tu consulta aqui o usa las acciones rapidas de arriba...'
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
        </div>        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button 
            onClick={() => handleQuickAction('jn_obras')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-xl border-2 border-emerald-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 21h18"/>
              <path d="M5 21V7l8-4v18"/>
              <path d="M19 21V11l-6-4"/>
            </svg>
            JN Obras
          </button>
          <button 
            onClick={() => handleQuickAction('jn_servicios')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-blue-50 hover:bg-blue-100 text-blue-800 rounded-xl border-2 border-blue-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            JN Servicios
          </button>
          <button 
            onClick={() => handleQuickAction('jn_suministros')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-xl border-2 border-amber-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M7.5 8a5.5 5.5 0 1 1 9 0"/>
              <path d="M12 8v13l-4-7 4-6z"/>
            </svg>
            JN Suministros
          </button>
          <button 
            onClick={() => handleQuickAction('jn_mantenimiento')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-purple-50 hover:bg-purple-100 text-purple-800 rounded-xl border-2 border-purple-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
            </svg>
            JN Mantenimiento
          </button>
          <button 
            onClick={() => handleQuickAction('jn_tecnologia')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-indigo-50 hover:bg-indigo-100 text-indigo-800 rounded-xl border-2 border-indigo-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
            JN Tecnología
          </button>
          <button 
            onClick={() => handleQuickAction('jn_formacion')}
            disabled={isThinking}
            className="quick-action-btn px-4 py-3 text-sm bg-green-50 hover:bg-green-100 text-green-800 rounded-xl border-2 border-green-200 disabled:opacity-50 font-medium"
          >
            <svg className="w-5 h-5 mb-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
              <path d="M6 12v5c3 3 9 3 12 0v-5"/>
            </svg>
            JN Formación
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
              onKeyDown={handleKeyDown}              className="form-textarea border-0 bg-gray-50 focus:bg-white"
              placeholder={getPlaceholder()}
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
      </div>    </section>
  )
}

export default ChatSection
