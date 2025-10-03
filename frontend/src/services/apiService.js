import axios from 'axios'

// Configuración del backend FastAPI
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 100000, 
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Interceptor para requests
    this.client.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => Promise.reject(error)
    )

    // Interceptor para responses
    this.client.interceptors.response.use(
      (response) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`)
        return response
      },
      (error) => {
        console.error('❌ API Error:', error.response?.data || error.message)
        
        // Si el backend no está disponible, mostrar error específico
        if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
          console.error('🔌 Backend not available. Make sure FastAPI is running on port 8000')
        }
        
        return Promise.reject(error)
      }
    )
  }  // Método principal: Generación de Justificación de la Necesidad
  async generateJN(userInput) {
    try {
      console.log('📋 generateJN userInput:', userInput)
      
      // Construir el payload exacto que espera el backend
      const body = {
        user_input: {
          expediente_id: userInput.expediente_id,
          seccion: userInput.seccion,
          user_text: userInput.user_text
        },
        structured_llm_choice: userInput.structured_llm_choice || 'openai',
        narrative_llm_choice: userInput.narrative_llm_choice || 'groq'
      }
      
      console.log('📤 Sending to backend:', body)
      const response = await this.client.post('/justificacion/generar_jn', body)
      
      // Formatear la respuesta para mostrar en el chat
      const jnData = response.data
      const formattedContent = this.formatJNResponse(jnData)
      
      return { success: true, content: formattedContent }
    } catch (error) {
      console.error('❌ Error generating JN (real):', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
        content: this.getMockJN(userInput)
      }
    }
  }
  // Formatear respuesta de JN del backend para mostrar en el chat
  formatJNResponse(jnData) {
    console.log('🔍 Procesando respuesta del backend:', jnData)
    
    // Extraer la narrativa limpia según la estructura de respuesta del backend
    let cleanNarrative = this.extractCleanNarrative(jnData)
    
    // Si no hay narrativa extraída, usar un formato básico
    if (!cleanNarrative) {
      cleanNarrative = 'Justificación de la Necesidad generada correctamente. Los datos estructurados han sido procesados por el sistema.'
    }
    
    const now = new Date().toLocaleString('es-ES')
    
    return `<div class="generated-content">
<h3 style="color: var(--cm-red); margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
  </svg>
  Justificación de la Necesidad (JN) - IA
</h3>

<div style="background: #f8f9fa; padding: 16px; border-left: 4px solid var(--cm-red); margin: 12px 0; border-radius: 8px; line-height: 1.6;">
${cleanNarrative}
</div>

<p><small style="display: flex; align-items: center; gap: 4px; color: #666;">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="10"/>
    <path d="M12 6l0 6l4 4"/>
  </svg>
  <strong>Generado:</strong> ${now} - Contenido creado con IA (OpenAI GPT-4)
</small></p>
</div>`
  }  // Extraer solo la narrativa limpia de la respuesta compleja del backend
  extractCleanNarrative(jnData) {
    try {
      console.log('🔍 Extrayendo narrativa de:', jnData)
      
      // Caso 1: Si hay un campo 'narrativa' directo (principal según el backend)
      if (jnData.narrativa && typeof jnData.narrativa === 'string') {
        console.log('✅ Narrativa encontrada en campo directo')
        return this.cleanNarrativeText(jnData.narrativa)
      }
      
      // Caso 2: Si la narrativa está en un objeto anidado
      if (jnData.data?.narrativa && typeof jnData.data.narrativa === 'string') {
        console.log('✅ Narrativa encontrada en data.narrativa')
        return this.cleanNarrativeText(jnData.data.narrativa)
      }
      
      // Caso 3: Si hay un campo 'response' que contiene la narrativa
      if (jnData.response && typeof jnData.response === 'string') {
        console.log('✅ Narrativa encontrada en response')
        return this.cleanNarrativeText(jnData.response)
      }
      
      // Caso 4: Si está en 'content', 'text' o 'texto'
      if (jnData.content && typeof jnData.content === 'string') {
        console.log('✅ Narrativa encontrada en content')
        return this.cleanNarrativeText(jnData.content)
      }
      
      if (jnData.text && typeof jnData.text === 'string') {
        console.log('✅ Narrativa encontrada en text')
        return this.cleanNarrativeText(jnData.text)
      }
      
      if (jnData.texto && typeof jnData.texto === 'string') {
        console.log('✅ Narrativa encontrada en texto')
        return this.cleanNarrativeText(jnData.texto)
      }
      
      // Caso 5: Buscar en campos anidados del objeto JustificacionNecesidadStructured
      if (typeof jnData === 'object' && jnData !== null) {
        // Buscar recursivamente en objetos anidados
        for (const [key, value] of Object.entries(jnData)) {
          if (typeof value === 'object' && value !== null) {
            if (value.narrativa && typeof value.narrativa === 'string') {
              console.log(`✅ Narrativa encontrada en ${key}.narrativa`)
              return this.cleanNarrativeText(value.narrativa)
            }
          }
          
          // Buscar en campos string largos que parezcan narrativa
          if (typeof value === 'string' && value.length > 50 && this.looksLikeNarrative(value)) {
            console.log(`✅ Narrativa encontrada en campo '${key}'`)
            return this.cleanNarrativeText(value)
          }
        }
      }
      
      console.warn('⚠️ No se encontró narrativa en la respuesta:', Object.keys(jnData))
      return null
      
    } catch (error) {
      console.error('❌ Error extrayendo narrativa:', error)
      return null
    }
  }
  
  // Limpiar el texto de la narrativa (remover JSON, caracteres especiales, etc.)
  cleanNarrativeText(text) {
    try {
      // Si el texto contiene JSON, intentar extraerlo
      if (text.includes('{') && text.includes('}')) {
        // Buscar si hay JSON embebido
        const jsonMatch = text.match(/\{[\s\S]*\}/)
        if (jsonMatch) {
          try {
            const jsonObj = JSON.parse(jsonMatch[0])
            
            // Si el JSON tiene campos de narrativa conocidos
            if (jsonObj.narrativa) return this.formatNarrativeText(jsonObj.narrativa)
            if (jsonObj.texto) return this.formatNarrativeText(jsonObj.texto)
            if (jsonObj.contenido) return this.formatNarrativeText(jsonObj.contenido)
            if (jsonObj.justificacion) return this.formatNarrativeText(jsonObj.justificacion)
            
            // Si es un objeto con múltiples campos de texto, combinarlos
            const textFields = Object.values(jsonObj)
              .filter(val => typeof val === 'string' && val.length > 20)
            
            if (textFields.length > 0) {
              return textFields.map(text => this.formatNarrativeText(text)).join('<br><br>')
            }
          } catch (jsonError) {
            console.warn('⚠️ No se pudo parsear JSON embebido:', jsonError)
          }
        }
        
        // Si no se pudo extraer JSON, removerlo y usar el texto restante
        text = text.replace(/\{[\s\S]*\}/g, '').trim()
      }
      
      return this.formatNarrativeText(text)
      
    } catch (error) {
      console.error('❌ Error limpiando narrativa:', error)
      return text
    }
  }
  
  // Formatear texto de narrativa para mostrar limpio
  formatNarrativeText(text) {
    if (!text || typeof text !== 'string') return ''
    
    return text
      .trim()
      .replace(/\n\n+/g, '<br><br>')  // Párrafos
      .replace(/\n/g, '<br>')         // Saltos de línea simples
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Negrita markdown
      .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Cursiva markdown
      .replace(/#{1,6}\s*(.*)/g, '<strong>$1</strong>')  // Headers markdown
  }
    // Verificar si un texto parece ser narrativa (heurística)
  looksLikeNarrative(text) {
    if (!text || typeof text !== 'string' || text.length < 50) return false
    
    // Palabras clave que indican que es narrativa de JN
    const jnKeywords = [
      'justificación', 'necesidad', 'objetivo', 'contratación', 'expediente',
      'administración', 'servicio', 'obra', 'suministro', 'procedimiento',
      'licitación', 'adjudicación', 'presupuesto', 'económico', 'normativa',
      'lcsp', 'rgpd', 'dnsh', 'igualdad', 'accesibilidad', 'público',
      'mediante', 'decreto', 'artículo', 'disposición', 'establece'
    ]
    
    const lowerText = text.toLowerCase()
    const keywordMatches = jnKeywords.filter(keyword => lowerText.includes(keyword)).length
    
    // Debe tener al menos 2 palabras clave y una longitud razonable
    return keywordMatches >= 2 || (keywordMatches >= 1 && text.length > 200)
  }

  // Chat inteligente con OpenAI (ajustado: solo usa generateJN para JN, mock para el resto)
  async chatWithBot(message, context = {}) {
    try {
      console.log('💬 Sending message to bot:', message)

      // Detectar tipo de solicitud
      const requestType = this.detectRequestType(message)

      if (requestType === 'jn') {
        // Para JN delegamos al endpoint real
        return await this.generateJN({ user_input: context })
      }

      // Si solo existe el endpoint de JN en el backend, devolvemos mock local para el resto
      console.warn('⚠️ Endpoint /chat no disponible - usando respuesta local mock para tipo:', requestType)
      return {
        success: true,
        content: this.getMockResponse(message, context),
        type: requestType
      }
    } catch (error) {
      console.error('❌ Error in chat:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
        content: this.getMockResponse(message, context)
      }
    }
  }

  // Detectar tipo de solicitud del usuario
  detectRequestType(message) {
    const lowerMsg = message.toLowerCase()
    
    if (lowerMsg.includes('jn') || lowerMsg.includes('justificación')) return 'jn'
    if (lowerMsg.includes('ppt') || lowerMsg.includes('pliego')) return 'ppt'
    if (lowerMsg.includes('cec') || lowerMsg.includes('presupuesto')) return 'cec'
    if (lowerMsg.includes('cr') || lowerMsg.includes('cuadro resumen')) return 'cr'
    if (lowerMsg.includes('expediente completo')) return 'complete'
    if (lowerMsg.includes('cumplimiento') || lowerMsg.includes('validar')) return 'validate'
    
    return 'general'
  }
  // Validación de cumplimiento normativo
  async validateCompliance(content) {
    try {
      console.log('✅ Validating compliance for content')
      const response = await this.client.post('/validate/compliance', { 
        content,
        checks: ['DNSH', 'RGPD', 'fraccionamiento']
      })
      return {
        success: true,
        results: response.data.validation_results || response.data
      }
    } catch (error) {
      console.error('❌ Error validating compliance:', error)
      return {
        success: false,
        error: error.message,
        results: this.getMockCompliance()
      }
    }
  }

  // Validación de coherencia entre documentos
  async validateCoherence(sections) {
    try {
      console.log('🔗 Validating coherence between sections')
      const response = await this.client.post('/validate/coherence', { sections })
      return {
        success: true,
        results: response.data.coherence_results || response.data
      }
    } catch (error) {
      console.error('❌ Error validating coherence:', error)
      return {
        success: false,
        error: error.message,
        results: this.getMockCoherence()
      }
    }
  }

  // Generar expediente completo
  async generateComplete(context) {
    try {
      console.log('🚀 Generating complete expedition')
      const response = await this.client.post('/generate/complete', context)
      return {
        success: true,
        sections: response.data.sections || response.data
      }
    } catch (error) {
      console.error('❌ Error generating complete expedition:', error)
      return {
        success: false,
        error: error.message,
        sections: this.getMockComplete(context)
      }
    }
  }

  // Health check del backend
  async healthCheck() {
    try {
      const response = await this.client.get('/health')
      return {
        success: true,
        status: response.data.status || 'OK',
        backend: true
      }
    } catch (error) {
      return {
        success: false,
        status: 'Backend not available',
        backend: false,
        error: error.message
      }
    }
  }
  // ============ MÉTODOS MOCK PARA FALLBACK ============

  getMockJN(context) {
    const now = new Date().toLocaleString('es-ES')
    return `<div class="generated-content">
<h3 style="color: var(--cm-red); margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
  </svg>
  Justificación de la Necesidad (JN)
</h3>
<p><strong>Generado:</strong> ${now}</p>
<p><strong>Proceso:</strong> ${context.proceso || 'No especificado'}</p>
<p><strong>Entidad:</strong> ${context.entidad || 'No especificada'}</p>

<h4>1. Necesidad identificada</h4>
<p>Se ha identificado la necesidad de contratar <em>${context.proceso || 'servicios especializados'}</em> para garantizar la continuidad del servicio público y el cumplimiento de los objetivos institucionales.</p>

<h4>2. Justificación normativa</h4>
<p>La contratación se ajusta a lo dispuesto en la Ley de Contratos del Sector Público, garantizando los principios de transparencia, concurrencia e igualdad de trato.</p>

<h4>3. Procedimiento propuesto</h4>
<p>Se propone procedimiento abierto con criterios de adjudicación equilibrados que permitan seleccionar la oferta más ventajosa.</p>

<p><small style="display: flex; align-items: center; gap: 4px;">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/>
    <line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>
  <strong>Modo offline:</strong> Contenido generado localmente. Conecta con el backend para obtener respuestas inteligentes de OpenAI.
</small></p>
</div>`
  }

  getMockResponse(message, context) {
    const responses = {      jn: `<div class="ai-response">
<h4 style="display: flex; align-items: center; gap: 8px;">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
  </svg>
  Sobre Justificación de la Necesidad
</h4>
<p>La JN debe incluir:</p>
<ul>
<li>Identificación clara de la necesidad</li>
<li>Justificación del procedimiento seleccionado</li>
<li>Criterios de adjudicación propuestos</li>
<li>Presupuesto estimativo</li>
</ul>
<p><em style="display: flex; align-items: center; gap: 4px;">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="10"/>
    <path d="M12 6l0 6l4 4"/>
  </svg>
  Usa la acción rápida "Generar JN" para crear el documento completo.
</em></p>
</div>`,      ppt: `<div class="ai-response">
<h4 style="display: flex; align-items: center; gap: 8px;">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
  </svg>
  Sobre Pliego de Prescripciones Técnicas
</h4>
<p>El PPT debe definir:</p>
<ul>
<li>Objeto y alcance del contrato</li>
<li>Especificaciones técnicas</li>
<li>Criterios de solvencia</li>
<li>Obligaciones del contratista</li>
</ul>
</div>`,      complete: `<div class="ai-response">
<h4 style="display: flex; align-items: center; gap: 8px;">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
  </svg>
  Expediente Completo
</h4>
<p>Para generar el expediente completo necesito:</p>
<ul>
<li style="display: flex; align-items: center; gap: 4px;">
  ${context.proceso ? 
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="green" stroke-width="2"><polyline points="20,6 9,17 4,12"/></svg>' : 
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="red" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' 
  }
  Descripción del proceso: ${context.proceso || 'Pendiente'}
</li>
<li style="display: flex; align-items: center; gap: 4px;">
  ${context.entidad ? 
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="green" stroke-width="2"><polyline points="20,6 9,17 4,12"/></svg>' : 
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="red" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' 
  }
  Entidad contratante: ${context.entidad || 'Pendiente'}
</li>
<li style="display: flex; align-items: center; gap: 4px;">
  ${context.fecha ? 
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="green" stroke-width="2"><polyline points="20,6 9,17 4,12"/></svg>' : 
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="red" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' 
  }
  Fecha límite: ${context.fecha || 'Pendiente'}
</li>
</ul>
<p>Completa el contexto para obtener documentos más precisos.</p>
</div>`,      default: `<div class="ai-response">
<h4 style="display: flex; align-items: center; gap: 8px;">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="3"/>
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
  </svg>
  Mini-CELIA (Modo Offline)
</h4>
<p>Entiendo tu consulta sobre: "<em>${message}</em>"</p>
<p>Actualmente estoy funcionando en modo offline. Para obtener respuestas inteligentes y generar documentos con IA:</p>
<ol>
<li style="display: flex; align-items: center; gap: 4px;">
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
  </svg>
  Inicia el backend FastAPI (puerto 8000)
</li>
<li style="display: flex; align-items: center; gap: 4px;">
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
    <circle cx="12" cy="16" r="1"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  </svg>
  Configura tu API key de OpenAI
</li>
<li style="display: flex; align-items: center; gap: 4px;">
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M1 4v6h6"/>
    <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
  </svg>
  Recarga la página
</li>
</ol>
<p><strong>Mientras tanto, puedes usar las acciones rápidas para generar contenido básico.</strong></p>
</div>`
    }

    const type = this.detectRequestType(message)
    return responses[type] || responses.default
  }

  getMockCompliance() {
    return {
      dnsh: { passed: true, details: 'DNSH: Sin impacto negativo identificado' },
      rgpd: { passed: true, details: 'RGPD: Cumple requisitos de protección de datos' },
      fraccionamiento: { passed: true, details: 'No fraccionamiento: Objeto contractual único' },
      overall: 'CUMPLE',
      recommendations: ['Verificar clausulado específico antes de publicación']
    }
  }

  getMockCoherence() {
    return {
      jn_ppt: { coherent: true, details: 'Objeto coherente entre JN y PPT' },
      ppt_cec: { coherent: true, details: 'Presupuesto alineado con especificaciones' },
      overall: 'COHERENTE',
      warnings: []
    }
  }  getMockComplete(context) {
    return {
      jn: this.getMockJN(context),
      ppt: `<h3 style="display: flex; align-items: center; gap: 8px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
        </svg>
        Pliego de Prescripciones Técnicas
      </h3>
      <p>Generado automáticamente para: ${context.proceso || 'el proceso'}</p>`,
      cec: `<h3 style="display: flex; align-items: center; gap: 8px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="1" x2="12" y2="23"/>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
        Cuadro Económico de Costes
      </h3>
      <p>Presupuesto estimativo para: ${context.proceso || 'el proceso'}</p>`,
      cr: `<h3 style="display: flex; align-items: center; gap: 8px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
          <path d="M9 9h6v6H9z"/>
        </svg>
        Cuadro Resumen
      </h3>
      <p>Resumen ejecutivo del expediente</p>`
    }
  }
}

// Exportar instancia singleton
export default new ApiService()
