import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import { apiService } from '../services/apiService'

const QuickActions = () => {
  const { 
    state, 
    setStepContent, 
    updateCompliance, 
    updateCoherence, 
    addMessage, 
    getProgress 
  } = useAppState()

  const handleQuickAction = async (action) => {
    switch (action) {
      case 'generar-jn':
        await generateSection('JN')
        break
      case 'generar-ppt':
        await generateSection('PPT')
        break
      case 'generar-cec':
        await generateSection('CEC')
        break
      case 'generar-cr':
        await generateSection('CR')
        break
      case 'validar-coherencia':
        await runCoherence()
        break
      case 'ver-cumplimiento':
        await runCompliance()
        break
    }
  }

  const generateSection = async (sectionId) => {
    try {
      addMessage('bot', `Generando ${getSectionName(sectionId)}...`)
      const result = await apiService.generateSection(sectionId, state.ctx)
      setStepContent(sectionId, result.content, result.citations)
      addMessage('bot', `${getSectionName(sectionId)} generada correctamente.`)
    } catch (error) {
      addMessage('bot', `Error generando ${getSectionName(sectionId)}: ${error.message}`)
    }
  }

  const runCompliance = async () => {
    try {
      addMessage('bot', 'Evaluando cumplimiento normativo...')
      const sections = {}
      state.steps.forEach(step => {
        if (step.content) sections[step.id] = step.content
      })
      const result = await apiService.runCompliance(sections)
      updateCompliance(result)
      
      const message = result.Missing.length 
        ? `Cumplimiento: faltan referencias a ${result.Missing.join(', ')}.`
        : 'Cumplimiento: correcto en DNSH/PRTR, RGPD y no fraccionamiento.'
      addMessage('bot', message)
    } catch (error) {
      addMessage('bot', `Error evaluando cumplimiento: ${error.message}`)
    }
  }

  const runCoherence = async () => {
    try {
      addMessage('bot', 'Validando coherencia inter-documental...')
      const sections = {}
      state.steps.forEach(step => {
        if (step.content) sections[step.id] = step.content
      })
      const result = await apiService.runCoherence(sections)
      updateCoherence(result)
      
      const message = result.ok 
        ? 'Coherencia: OK (lotes/pesos/plazos consistentes).'
        : `Coherencia: hallé observaciones: ${result.notes.join(', ')}`
      addMessage('bot', message)
    } catch (error) {
      addMessage('bot', `Error validando coherencia: ${error.message}`)
    }
  }

  const getSectionName = (id) => {
    const names = {
      JN: 'Justificación de la Necesidad',
      PPT: 'Pliego Técnico',
      CEC: 'Presupuesto (CEC)',
      CR: 'Cuadro Resumen'
    }
    return names[id] || id
  }

  const getComplianceBadge = () => {
    const { compliance } = state
    if (!compliance.Missing) return { text: 'Pendiente', class: 'border-gray-300' }
    
    return compliance.Missing.length === 0 
      ? { text: 'Correcto', class: 'border-emerald-300 text-emerald-700 bg-emerald-50' }
      : { text: 'Faltan referencias', class: 'border-rose-300 text-rose-700 bg-rose-50' }
  }

  const getCoherenceBadge = () => {
    const { coherence } = state
    if (!coherence.checked) return { text: 'Sin validar', class: 'border-gray-300' }
    
    return coherence.ok
      ? { text: 'Coherente', class: 'border-emerald-300 text-emerald-700 bg-emerald-50' }
      : { text: 'Con observaciones', class: 'border-amber-300 text-amber-700 bg-amber-50' }
  }

  const complianceBadge = getComplianceBadge()
  const coherenceBadge = getCoherenceBadge()

  return (
    <section className="lg:col-span-6 bg-white border border-gray-200 rounded-xl p-4 shadow-soft">
      <h2 className="text-base font-semibold mb-2">Acciones rápidas</h2>
      
      <div className="flex flex-wrap gap-2 mb-3">
        <button 
          onClick={() => handleQuickAction('generar-jn')}
          className="chip px-3 py-1.5 rounded-full text-sm"
        >
          Generar JN
        </button>
        <button 
          onClick={() => handleQuickAction('generar-ppt')}
          className="chip px-3 py-1.5 rounded-full text-sm"
        >
          Generar PPT
        </button>
        <button 
          onClick={() => handleQuickAction('generar-cec')}
          className="chip px-3 py-1.5 rounded-full text-sm"
        >
          Generar CEC
        </button>
        <button 
          onClick={() => handleQuickAction('generar-cr')}
          className="chip px-3 py-1.5 rounded-full text-sm"
        >
          Generar CR
        </button>
        <button 
          onClick={() => handleQuickAction('validar-coherencia')}
          className="chip px-3 py-1.5 rounded-full text-sm"
        >
          Validar coherencia
        </button>
        <button 
          onClick={() => handleQuickAction('ver-cumplimiento')}
          className="chip px-3 py-1.5 rounded-full text-sm"
        >
          Ver cumplimiento
        </button>
      </div>
      
      <div className="grid sm:grid-cols-3 gap-3 text-sm">
        <div className="rounded-lg border border-gray-200 p-3">
          <div className="text-[11px] text-muted mb-1">Progreso del expediente</div>
          <div className="w-full bg-gray-100 rounded-full h-2">
            <div 
              className="h-2 rounded-full transition-all duration-300"
              style={{
                width: `${getProgress()}%`, 
                background: 'var(--cm-red)'
              }}
            />
          </div>
        </div>
        
        <div className="rounded-lg border border-gray-200 p-3">
          <div className="text-[11px] text-muted mb-1">Cumplimiento</div>
          <div className={`text-xs px-2 py-1 rounded border inline-block ${complianceBadge.class}`}>
            {complianceBadge.text}
          </div>
        </div>
        
        <div className="rounded-lg border border-gray-200 p-3">
          <div className="text-[11px] text-muted mb-1">Coherencia</div>
          <div className={`text-xs px-2 py-1 rounded border inline-block ${coherenceBadge.class}`}>
            {coherenceBadge.text}
          </div>
        </div>
      </div>
      
      <p className="mt-3 text-xs text-muted">
        Nota: acciones avanzadas (orquestador, edición del borrador y exportación de manifiesto) pueden requerir perfil Admin.
      </p>
    </section>
  )
}

export default QuickActions
