import axios from 'axios'

const API_BASE_URL = '/api'

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor para agregar token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor para manejar errores
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user_data')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Métodos para secciones
  async generateSection(sectionId, context) {
    try {
      const response = await this.client.post('/generate', {
        section: sectionId,
        context
      })
      return response.data
    } catch (error) {
      console.error('Error generating section:', error)
      // Fallback a generación mock si el backend no está disponible
      return this.mockGenerateSection(sectionId, context)
    }
  }

  async validateSection(sectionId, content) {
    try {
      const response = await this.client.post('/validate', {
        section: sectionId,
        content
      })
      return response.data
    } catch (error) {
      console.error('Error validating section:', error)
      return this.mockValidateSection(sectionId, content)
    }
  }

  async runCompliance(content) {
    try {
      const response = await this.client.post('/compliance', { content })
      return response.data
    } catch (error) {
      console.error('Error checking compliance:', error)
      return this.mockRunCompliance(content)
    }
  }

  async runCoherence(sections) {
    try {
      const response = await this.client.post('/coherence', { sections })
      return response.data
    } catch (error) {
      console.error('Error checking coherence:', error)
      return this.mockRunCoherence(sections)
    }
  }

  // Mock implementations para cuando el backend no esté disponible
  mockGenerateSection(sectionId, context) {
    const now = new Date().toLocaleString()
    const templates = {
      JN: `# Justificación de la Necesidad (JN)
Fecha: ${now}
Proceso: ${context.proceso || '—'}
Entidad: ${context.entidad || '—'}

1. Necesidad y procedimiento
La contratación se justifica por la existencia de una necesidad cierta y actual, conforme a la normativa aplicable [Fuente: Golden Repo · Contratación Pública].

2. Objeto y fines
Se requiere ${context.proceso || 'el servicio/obra/suministro'} para asegurar continuidad y calidad del servicio público.

3. Eficiencia y eficacia
La solución seleccionada maximiza la eficiencia, evitando fraccionamientos indebidos y garantizando concurrencia [Norma de referencia].

4. Procedimiento propuesto
Se propone procedimiento abierto con publicidad suficiente, criterios de adjudicación equilibrados y ponderación total de 100%.`,
      
      PPT: `# Pliego Técnico (PPT)
Fecha: ${now}

Alcance
• Actividades principales vinculadas a ${context.proceso || 'el objeto'}.
• Entregables y criterios de aceptación.

Criterios Técnicos
• Metodología de ejecución.
• Medios y solvencias técnicas.

Obligaciones
• RGPD y seguridad de la información.
• DNSH/PRTR cuando proceda.

Hitos y Plazos
• Definición de hitos y plazos coherentes con la fecha límite ${context.fecha ? '(' + context.fecha + ')' : ''}.`,

      CEC: `# Presupuesto (CEC)
Fecha: ${now}

Estructura de costes
• Directos, Indirectos, Impuestos.

Cuantificación del PPT
• Los costes se derivan del alcance definido en el PPT.

Ponderación Económica
• Pesos económicos total = 100%.`,

      CR: `# Cuadro Resumen (CR)
Fecha: ${now}

Criterios de adjudicación
• Técnicos: 60%
• Económicos: 40%
Total: 100%

Plazos y solvencias
• Plazos alineados con PPT y JN.
• Solvencias técnicas y económicas según normativa.`
    }

    const citations = {
      JN: ['CP_General_2024', 'Concurrencia_Art.xxx'],
      PPT: ['PPT_Modelo_v1', 'RGPD_Guia'],
      CEC: ['CEC_Estructura', 'Fiscalidad_IVA'],
      CR: ['CR_Ponderaciones', 'Solvencias_Reglamento']
    }

    return {
      content: templates[sectionId] || 'Contenido generado automáticamente.',
      citations: citations[sectionId] || []
    }
  }

  mockValidateSection(sectionId, content) {
    const errors = []
    
    if (!content?.trim()) {
      errors.push('No hay contenido generado.')
    }
    
    if (sectionId === 'CR' && !/Total:\s*100%/i.test(content)) {
      errors.push('Los pesos deben sumar 100% (incluye "Total: 100%").')
    }
    
    if (sectionId === 'CEC' && !/100%/i.test(content)) {
      errors.push('Incluye referencia a pesos = 100% en CEC.')
    }
    
    if (sectionId === 'PPT' && !/RGPD/i.test(content)) {
      errors.push('Incluye mención a RGPD en obligaciones.')
    }
    
    if (sectionId === 'JN' && !/necesidad/i.test(content)) {
      errors.push('Incluye el fundamento de la necesidad.')
    }

    return {
      valid: errors.length === 0,
      errors
    }
  }

  mockRunCompliance(content) {
    const jn = content.JN || ''
    const ppt = content.PPT || ''
    
    const compliance = {
      DNSH: /DNSH/i.test(ppt),
      PRTR: /PRTR/i.test(ppt),
      RGPD: /RGPD/i.test(ppt),
      Fracc: /fraccionam/i.test(jn)
    }
    
    const missing = []
    if (!compliance.DNSH) missing.push('DNSH')
    if (!compliance.PRTR) missing.push('PRTR')
    if (!compliance.RGPD) missing.push('RGPD')
    if (!compliance.Fracc) missing.push('No fraccionamiento')
    
    return {
      ...compliance,
      Missing: missing
    }
  }

  mockRunCoherence(sections) {
    const cr = sections.CR || ''
    const ppt = sections.PPT || ''
    const cec = sections.CEC || ''
    const notes = []

    if (!/Total:\s*100%/i.test(cr)) {
      notes.push('CR: los pesos no suman 100%.')
    }
    
    if (!/100%/i.test(cec)) {
      notes.push('CEC: añade referencia a pesos = 100%.')
    }
    
    return {
      checked: true,
      ok: notes.length === 0,
      notes
    }
  }
}

export const apiService = new ApiService()
