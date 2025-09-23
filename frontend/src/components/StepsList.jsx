import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import { apiService } from '../services/apiService'

const StepsList = () => {
  const { 
    state, 
    setStepContent, 
    addMessage, 
    addToDraft, 
    setShowDraftModal,
    wordCount 
  } = useAppState()

  const handleGenerate = async (stepId) => {
    try {
      addMessage('bot', `Generando ${getStepName(stepId)}...`)
      const result = await apiService.generateSection(stepId, state.ctx)
      setStepContent(stepId, result.content, result.citations)
      addMessage('bot', `${getStepName(stepId)} generada correctamente.`)
    } catch (error) {
      addMessage('bot', `Error generando ${getStepName(stepId)}: ${error.message}`)
    }
  }

  const handleValidate = async (stepId) => {
    const step = state.steps.find(s => s.id === stepId)
    if (!step?.content) {
      addMessage('bot', `No hay contenido para validar en ${getStepName(stepId)}.`)
      return
    }

    try {
      const result = await apiService.validateSection(stepId, step.content)
      if (result.valid) {
        addMessage('bot', `${getStepName(stepId)} validada. Sin observaciones.`)
        // Update step status to reviewed
        const updatedSteps = state.steps.map(s => 
          s.id === stepId ? { ...s, status: 'revisado' } : s
        )
        // This would need to be handled by the context
      } else {
        const errors = result.errors.join('<br/>• ')
        addMessage('bot', `Validación de ${getStepName(stepId)}:<br/>• ${errors}`)
      }
    } catch (error) {
      addMessage('bot', `Error validando ${getStepName(stepId)}: ${error.message}`)
    }
  }

  const handleEdit = (stepId) => {
    setShowDraftModal(true)
    // This would need additional logic to focus on the specific step in the draft modal
  }

  const handleAddToDraft = (step) => {
    if (step.content) {
      addToDraft(step.name, step.content)
      addMessage('bot', `Sección "${step.name}" añadida al borrador.`)
    }
  }

  const handleCopy = async (content) => {
    try {
      await navigator.clipboard.writeText(content)
      // Simple toast notification
      showToast('Texto copiado')
    } catch (error) {
      showToast('No se pudo copiar')
    }
  }

  const showToast = (message) => {
    const toast = document.createElement('div')
    toast.className = 'fixed bottom-4 right-4 bg-white border border-gray-200 text-ink px-4 py-2 rounded-lg shadow-soft z-50'
    toast.textContent = message
    document.body.appendChild(toast)
    setTimeout(() => {
      toast.style.opacity = '0'
      setTimeout(() => document.body.removeChild(toast), 300)
    }, 1600)
  }

  const getStepName = (id) => {
    const step = state.steps.find(s => s.id === id)
    return step?.name || id
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'generado':
        return 'bg-emerald-50 border-emerald-200'
      case 'revisado':
        return 'bg-blue-50 border-blue-200'
      default:
        return 'bg-[#FFFDFD] border-[#F3D2D7]'
    }
  }

  const getStatusDotColor = (status) => {
    switch (status) {
      case 'generado':
        return 'bg-emerald-600'
      case 'revisado':
        return 'bg-blue-600'
      default:
        return 'bg-[var(--cm-red)]'
    }
  }

  return (
    <div className="space-y-3">
      {state.steps.map((step, index) => (
        <div key={step.id} className={`rounded-xl border ${getStatusColor(step.status)} p-3`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className={`status-dot ${getStatusDotColor(step.status)} inline-block`}></span>
              <div className="font-medium text-sm">{index + 1}. {step.name}</div>
            </div>
            <div className={`text-xs px-2 py-1 rounded border ${
              step.status === 'pendiente' 
                ? 'border-gray-300 text-muted' 
                : 'border-gray-300 text-ink'
            }`}>
              {step.status.charAt(0).toUpperCase() + step.status.slice(1)}
            </div>
          </div>
          
          <div className="mt-2 grid sm:grid-cols-3 gap-2">
            <button 
              onClick={() => handleGenerate(step.id)}
              className="px-2.5 py-1.5 rounded-md border cm-outline text-xs"
            >
              Generar
            </button>
            <button 
              onClick={() => handleValidate(step.id)}
              className="px-2.5 py-1.5 rounded-md border cm-outline text-xs"
            >
              Validar
            </button>
            <button 
              onClick={() => handleEdit(step.id)}
              className="px-2.5 py-1.5 rounded-md border cm-outline text-xs"
            >
              Editar
            </button>
          </div>
          
          {step.content && (
            <div className="mt-2 rounded-md bg-white border border-gray-200 p-2">
              <div className="flex items-center justify-between">
                <div className="text-xs text-muted">
                  Vista previa ({wordCount(step.content)} palabras)
                </div>
                <div className="flex items-center gap-2">
                  <button 
                    onClick={() => handleAddToDraft(step)}
                    className="px-2 py-1 rounded border cm-outline text-[11px]"
                  >
                    Añadir al borrador
                  </button>
                  <button 
                    onClick={() => handleCopy(step.content)}
                    className="px-2 py-1 rounded border cm-outline text-[11px]"
                  >
                    Copiar
                  </button>
                </div>
              </div>
              <pre className="text-xs whitespace-pre-wrap mt-1">
                {step.content.slice(0, 600)}{step.content.length > 600 ? '…' : ''}
              </pre>
              {step.citations && step.citations.length > 0 && (
                <div className="mt-2 text-[11px] text-muted">
                  Citas: {step.citations.map(c => `[${c}]`).join(' ')}
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default StepsList
