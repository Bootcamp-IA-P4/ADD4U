import React, { useState, useRef, useEffect } from 'react'
import { useAppState } from '../contexts/AppStateContext'
import apiService from '../services/apiService'
import LicitacionExamples from './LicitacionExamples'
import ClarificationPrompts from './ClarificationPrompts'

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
      console.log('[GEN] Generando JN con datos:', { expedienteId, userText, selectedType })
      
      const formData = {
        expediente_id: expedienteId,
        seccion: "JN.1", 
        user_text: userText
      }

      console.log('[API] Enviando datos a la API (orquestador):', formData)
      
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
      addMessage('bot', `<strong>[ERROR] Error al conectar con la API:</strong> ${error.message}<br><br>Verifica que el backend esté funcionando en <code>http://localhost:8000</code> y que tengas las variables de entorno configuradas.`)
    }

    // Reset conversation state
    setConversationState({
      waitingFor: null,
      selectedJNType: null,
      expediente_id: null,
      user_text: null
    })
  }
  
  // Nuevo: Manejar selección de ejemplo (vía rápida)
  const handleExampleSelection = async (exampleData) => {
    // 1. Mostrar el ejemplo seleccionado como mensaje del usuario
    const userMessage = `<strong>${exampleData.title}</strong><br><br>${exampleData.text}`
    addMessage('user', userMessage)
    
    // 2. Generar expediente_id automático basado en categoría y timestamp
    const categoryPrefix = exampleData.category.toUpperCase().substring(0, 3)
    const timestamp = Date.now().toString().slice(-4)
    const autoExpedienteId = `${categoryPrefix}-${timestamp}`
    
    // 3. Mostrar mensaje de confirmación simple con el expediente auto-generado
    const confirmMessage = `<strong>Expediente:</strong> ${autoExpedienteId}<br>` +
      `<strong>Sección:</strong> JN.1<br><br>` +
      `Generando justificación...`
    
    addMessage('bot', confirmMessage)
    setIsThinking(true)
    
    // 4. Pequeño delay para permitir que React actualice la UI
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // 5. Lanzar generación directa sin preguntar nada
    try {
      const formData = {
        expediente_id: autoExpedienteId,
        seccion: "JN.1",
        user_text: exampleData.text
      }
      
      const result = await apiService.generateJN(formData)
      
      setIsThinking(false)
      
      if (result.success) {
        addMessage('bot', result.content)
      } else {
        addMessage('bot', result.content || 'Error al generar la JN. Por favor, inténtalo de nuevo.')
        if (result.error) {
          console.error('[ERROR]', result.error)
        }
      }
    } catch (error) {
      setIsThinking(false)
      console.error('[ERROR]', error)
      addMessage('bot', `Error al generar: ${error.message}`)
    }
  }
  
  const handleQuickAction = (action) => {
    if (action.startsWith('jn_')) {
      const jnDescription = getJNTypeDescription(action)
      
      // Generar expediente_id automático
      const categoryMap = {
        'jn_obras': 'OBR',
        'jn_servicios': 'SER',
        'jn_suministros': 'SUM',
        'jn_consultoria': 'CON',
        'jn_tecnologia': 'TEC',
        'jn_mantenimiento': 'MAN'
      }
      
      const prefix = categoryMap[action] || 'GEN'
      const timestamp = Date.now().toString().slice(-4)
      const autoExpedienteId = `${prefix}-${timestamp}`
      
      // Mostrar mensaje pidiendo solo la descripción
      const message = `<strong>${jnDescription}</strong><br><br>` +
        `Expediente: <strong>${autoExpedienteId}</strong> (auto-generado)<br>` +
        `Sección: <strong>JN.1</strong><br><br>` +
        `Describe detalladamente lo que necesitas contratar:<br>` +
        `• ¿Qué servicio, obra o suministro necesitas?<br>` +
        `• ¿Cuál es el alcance y las cantidades?<br>` +
        `• ¿Dónde se ejecutará?<br>` +
        `• ¿Por qué es necesario?`

      addMessage('bot', message)
      
      // Guardar estado para esperar la descripción
      setConversationState({
        waitingFor: 'user_description',
        selectedJNType: action,
        expediente_id: autoExpedienteId,
        user_text: null
      })
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

      const message = `<strong>Expediente: ${expedienteId}</strong><br><br>` +
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

      const confirmMessage = `<strong>Información completa recibida</strong><br><br>` +
        `<strong>Expediente:</strong> ${conversationState.expediente_id}<br>` +
        `<strong>Tipo:</strong> ${getJNTypeDescription(conversationState.selectedJNType)}<br>` +
        `<strong>Descripción:</strong> ${text.substring(0, 100)}${text.length > 100 ? '...' : ''}<br><br>` +
        `<strong>Generando tu Justificación de la Necesidad...</strong>`

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
          <div className="h-10 w-10 flex items-center justify-center flex-shrink-0">
            <img src="/images/icono.png" alt="Bot" className="h-10 w-10 object-contain" />
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

  const { saveState, loadState } = useAppState()

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
    const toast = document.createElement('div')
    toast.className = 'fixed bottom-4 right-4 bg-white border-2 border-brand-green text-ink px-4 py-2 rounded-lg shadow-lg z-50'
    toast.textContent = message
    document.body.appendChild(toast)
    setTimeout(() => {
      toast.style.opacity = '0'
      setTimeout(() => document.body.removeChild(toast), 300)
    }, 1600)
  }

  return (
    <section className="w-full h-full flex flex-col">
      {/* Header interno con logo y botones - FONDO BLANCO */}
      <div className="flex items-center justify-between p-3 bg-white border-b-2 border-gray-300">
        {/* Logo y título */}
        <div className="flex items-center gap-3">
          <div className="h-14 w-14 flex items-center justify-center">
            <img src="/images/icono4.png" alt="Mini-CELIA" className="h-14 w-14 object-contain" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-brand-blue">Mini-CELIA</h2>
            <p className="text-xs text-brand-green font-medium">Copilot Inteligente de Licitaciones</p>
          </div>
        </div>

        {/* Botones y estado */}
        <div className="flex items-center gap-2">
          <button 
            onClick={handleSave} 
            className="px-2 py-1 rounded-lg border border-brand-green bg-white text-brand-green text-xs font-semibold hover:bg-brand-green hover:text-white transition-all duration-200"
          >
            Guardar
          </button>
          
          <button 
            onClick={handleLoad} 
            className="px-2 py-1 rounded-lg border border-brand-blue bg-white text-brand-blue text-xs font-semibold hover:bg-brand-blue hover:text-white transition-all duration-200"
          >
            Cargar
          </button>
          
          <div className={'flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium ' + getStatusClass()}>
            {backendStatus.checking ? (
              <>
                <svg className="w-3 h-3 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                <span className="hidden sm:inline">Verificando...</span>
              </>
            ) : backendStatus.connected ? (
              <>
                <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10"/>
                </svg>
                <span className="hidden sm:inline">Conectado</span>
              </>
            ) : (
              <>
                <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10"/>
                </svg>
                <span className="hidden sm:inline">Offline</span>
              </>
            )}
          </div>
        </div>
      </div>
      
      {/* Área de chat scrollable */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Ejemplos de Licitación */}
        {state.chat.filter(m => m.role === 'user').length === 0 && (
          <LicitacionExamples onSelectExample={handleExampleSelection} />
        )}
        
        {/* Sistema de Re-pregunta */}
        {inputValue.length > 30 && !isThinking && (
          <ClarificationPrompts 
            userInput={inputValue} 
            onSendClarification={(clarification) => {
              setInputValue(inputValue + ' ' + clarification)
              textareaRef.current?.focus()
            }} 
          />
        )}
        
        <div 
          ref={chatBoxRef}
          className="space-y-6"
        >
          {state.chat.map(renderMessage)}
        
          {isThinking && (
            <div className="flex items-start gap-4">
              <div className="h-10 w-10 flex items-center justify-center flex-shrink-0">
                <img src="/images/icono.png" alt="Bot pensando" className="h-10 w-10 object-contain animate-spin" />
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
      </div>

      {/* Input area con sugerencias rápidas encima */}
      <div className="p-4 border-t-2 border-gray-300">
        {/* Sugerencias rápidas - alineadas a la izquierda */}
        <div className="flex flex-wrap gap-2 mb-3">
          <button 
            onClick={() => handleQuickAction('jn_obras')}
            disabled={isThinking}
            className="px-3 py-1.5 text-xs bg-brand-blue hover:bg-blue-600 text-white rounded-lg border border-brand-blue disabled:opacity-50 transition-all font-medium"
          >
            Obras
          </button>
          <button 
            onClick={() => handleQuickAction('jn_servicios')}
            disabled={isThinking}
            className="px-3 py-1.5 text-xs bg-brand-blue hover:bg-blue-600 text-white rounded-lg border border-brand-blue disabled:opacity-50 transition-all font-medium"
          >
            Servicios
          </button>
          <button 
            onClick={() => handleQuickAction('jn_suministros')}
            disabled={isThinking}
            className="px-3 py-1.5 text-xs bg-brand-blue hover:bg-blue-600 text-white rounded-lg border border-brand-blue disabled:opacity-50 transition-all font-medium"
          >
            Suministros
          </button>
          <button 
            onClick={() => handleQuickAction('jn_mantenimiento')}
            disabled={isThinking}
            className="px-3 py-1.5 text-xs bg-brand-blue hover:bg-blue-600 text-white rounded-lg border border-brand-blue disabled:opacity-50 transition-all font-medium"
          >
            Mantenimiento
          </button>
          <button 
            onClick={() => handleQuickAction('jn_tecnologia')}
            disabled={isThinking}
            className="px-3 py-1.5 text-xs bg-brand-blue hover:bg-blue-600 text-white rounded-lg border border-brand-blue disabled:opacity-50 transition-all font-medium"
          >
            Tecnología
          </button>
          <button 
            onClick={() => handleQuickAction('jn_formacion')}
            disabled={isThinking}
            className="px-3 py-1.5 text-xs bg-brand-blue hover:bg-blue-600 text-white rounded-lg border border-brand-blue disabled:opacity-50 transition-all font-medium"
          >
            Formación
          </button>
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
        </div>
      </div>
    </section>
  )
}

export default ChatSection

