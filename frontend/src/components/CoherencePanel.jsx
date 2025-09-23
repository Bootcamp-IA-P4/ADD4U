import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import { apiService } from '../services/apiService'

const CoherencePanel = () => {
  const { state, updateCoherence, addMessage } = useAppState()

  const handleRunCoherence = async () => {
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

  return (
    <div className="mt-3 rounded-lg border border-gray-200 p-3">
      <div className="flex items-center justify-between">
        <div className="font-medium text-sm">Coherencia inter‑documental</div>
        <button 
          onClick={handleRunCoherence}
          className="px-2.5 py-1.5 rounded-md border cm-outline text-xs"
        >
          Validar
        </button>
      </div>
      
      <p className="text-sm mt-2 text-muted">
        {state.coherence.checked 
          ? (state.coherence.notes.join(' · ') || 'Sin observaciones.')
          : 'Verifica lotes, pesos (=100%) y consistencia de plazos e importes.'
        }
      </p>
    </div>
  )
}

export default CoherencePanel
