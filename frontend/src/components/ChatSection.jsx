import React, { useState, useRef, useEffect } from 'react'
import { useAppState } from '../contexts/AppStateContext'

const ChatSection = () => {
  const { state, addMessage, escapeHtml } = useAppState()
  const [inputValue, setInputValue] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const chatBoxRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    // Welcome message on first load
    if (state.chat.length === 0) {
      const welcomeMessage = `Mini‑CELIA (PoC) · Genera y valida JN, PPT, CEC y CR con enfoque de cumplimiento.
• Usa las "Acciones rápidas" o pide "Generar JN/PPT/CEC/CR".
• "Ver cumplimiento" revisa DNSH/PRTR, RGPD y no fraccionamiento.
• "Validar coherencia" comprueba lotes, pesos (=100%) y plazos.`
      
      addMessage('bot', welcomeMessage.replace(/\n/g, '<br/>'))
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

  const handleSubmit = async (e) => {
    e.preventDefault()
    const text = inputValue.trim()
    if (!text) return

    addMessage('user', escapeHtml(text))
    setInputValue('')
    setIsThinking(true)

    // Simulate bot thinking
    setTimeout(() => {
      setIsThinking(false)
      botReply(text)
    }, 1000)
  }

  const botReply = (text) => {
    const lowerText = text.toLowerCase()
    
    // Check for missing context
    const missing = []
    if (!state.ctx.proceso) missing.push('proceso')
    if (!state.ctx.entidad) missing.push('entidad')
    if (!state.ctx.fecha) missing.push('fecha límite')
    
    if (missing.length > 0) {
      addMessage('bot', `Me falta: ${missing.join(', ')}. Complétalo arriba para afinar la redacción.`)
      return
    }

    // Simple bot responses based on keywords
    if (lowerText.includes('generar jn') || lowerText.includes('justificación')) {
      addMessage('bot', 'Sección Justificación de la Necesidad generada. Puedes "Editar", "Validar" y añadirla al borrador desde el panel derecho.')
    } else if (lowerText.includes('generar ppt') || lowerText.includes('pliego')) {
      addMessage('bot', 'Sección Pliego Técnico generada. Puedes "Editar", "Validar" y añadirla al borrador desde el panel derecho.')
    } else if (lowerText.includes('generar cec') || lowerText.includes('presupuesto')) {
      addMessage('bot', 'Sección Presupuesto (CEC) generada. Puedes "Editar", "Validar" y añadirla al borrador desde el panel derecho.')
    } else if (lowerText.includes('generar cr') || lowerText.includes('cuadro resumen')) {
      addMessage('bot', 'Sección Cuadro Resumen (CR) generada. Puedes "Editar", "Validar" y añadirla al borrador desde el panel derecho.')
    } else if (lowerText.includes('cumplimiento')) {
      addMessage('bot', 'Evaluando cumplimiento normativo: DNSH/PRTR, RGPD y no fraccionamiento.')
    } else if (lowerText.includes('coherencia')) {
      addMessage('bot', 'Validando coherencia inter-documental: lotes, pesos y plazos.')
    } else {
      addMessage('bot', '¿Quieres que orqueste el flujo completo ahora (JN → PPT → CEC → CR) o generamos una sección concreta?')
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
        <div key={message.id} className="flex items-start gap-3">
          <div className="h-8 w-8 rounded-md flex items-center justify-center" style={{background: 'var(--cm-red)'}}>
            <span className="h-2 w-2 rounded-full bg-white pulse"></span>
          </div>
          <div 
            className="max-w-[85%] md:max-w-[75%] rounded-xl bot-bubble px-4 py-3 text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: message.content }}
          />
        </div>
      )
    } else {
      return (
        <div key={message.id} className="flex items-start gap-3 justify-end">
          <div 
            className="max-w-[85%] md:max-w-[75%] rounded-xl user-bubble px-4 py-3 text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: message.content }}
          />
        </div>
      )
    }
  }

  return (
    <section className="lg:col-span-7 bg-white border border-gray-200 rounded-xl p-4 shadow-soft">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-base font-semibold">Chat</h2>
        <div className="text-xs text-muted">Interactúa como copilot: pregunta, propone y corrige</div>
      </div>
      
      <div 
        ref={chatBoxRef}
        className="h-[58vh] overflow-y-auto scrollbar pr-1 space-y-3"
      >
        {state.chat.map(renderMessage)}
        
        {isThinking && (
          <div className="flex items-start gap-3">
            <div className="h-8 w-8 rounded-md flex items-center justify-center" style={{background: 'var(--cm-red)'}}>
              <span className="h-2 w-2 rounded-full bg-white pulse"></span>
            </div>
            <div className="max-w-[85%] md:max-w-[75%] rounded-xl bot-bubble px-4 py-3 text-sm leading-relaxed">
              <span className="text-muted">Procesando…</span>
            </div>
          </div>
        )}
      </div>
      
      <form onSubmit={handleSubmit} className="mt-4 flex items-end gap-3">
        <div className="flex-1">
          <label htmlFor="userInput" className="sr-only">Escribe tu mensaje</label>
          <textarea
            ref={textareaRef}
            id="userInput"
            rows="2"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="form-textarea"
            placeholder="Ej: Genera JN con necesidad y procedimiento; cita fuentes del repositorio 'golden'…"
          />
        </div>
        <button 
          type="submit"
          disabled={!inputValue.trim() || isThinking}
          className="px-4 py-2 rounded-lg cm-btn font-medium disabled:opacity-50"
        >
          Enviar
        </button>
      </form>
    </section>
  )
}

export default ChatSection
