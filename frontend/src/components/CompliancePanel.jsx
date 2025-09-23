import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import { apiService } from '../services/apiService'

const CompliancePanel = () => {
  const { state, updateCompliance, addMessage } = useAppState()

  const handleRunCompliance = async () => {
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

  const getComplianceItems = () => {
    const { compliance } = state
    return [
      { 
        label: 'DNSH/PRTR', 
        ok: compliance.DNSH && compliance.PRTR,
        status: (compliance.DNSH && compliance.PRTR) ? 'OK' : 'Pendiente'
      },
      { 
        label: 'RGPD', 
        ok: compliance.RGPD,
        status: compliance.RGPD ? 'OK' : 'Pendiente'
      },
      { 
        label: 'No fraccionamiento', 
        ok: compliance.Fracc,
        status: compliance.Fracc ? 'OK' : 'Pendiente'
      }
    ]
  }

  const complianceItems = getComplianceItems()

  return (
    <div className="mt-4 rounded-lg border border-gray-200 p-3">
      <div className="flex items-center justify-between">
        <div className="font-medium text-sm">Cumplimiento normativo</div>
        <button 
          onClick={handleRunCompliance}
          className="px-2.5 py-1.5 rounded-md border cm-outline text-xs"
        >
          Evaluar
        </button>
      </div>
      
      <ul className="text-sm mt-2 space-y-1">
        {complianceItems.map((item, index) => (
          <li key={index} className="flex items-center justify-between">
            <span>{item.label}</span>
            <span className={`text-xs px-2 py-0.5 rounded border ${
              item.ok 
                ? 'border-emerald-300 text-emerald-700 bg-emerald-50'
                : 'border-rose-300 text-rose-700 bg-rose-50'
            }`}>
              {item.status}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default CompliancePanel
