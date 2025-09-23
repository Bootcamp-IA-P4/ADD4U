import React from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useAppState } from '../contexts/AppStateContext'
import StepsList from './StepsList'
import CompliancePanel from './CompliancePanel'
import CoherencePanel from './CoherencePanel'

const AdminPanel = () => {
  const { isAdmin } = useAuth()
  const { 
    state, 
    setStepContent, 
    addMessage, 
    setShowDraftModal 
  } = useAppState()

  if (!isAdmin) return null

  const handleGenerateAll = async () => {
    addMessage('bot', 'Generando todas las secciones en orden...')
    
    // Simulate generating all sections
    const sections = ['JN', 'PPT', 'CEC', 'CR']
    
    for (const sectionId of sections) {
      // Mock generation - in real app this would call the API
      setTimeout(() => {
        const mockContent = `# ${getSectionName(sectionId)}
Generado automáticamente el ${new Date().toLocaleString()}

${sectionId === 'CR' ? 'Total: 100%' : 'Contenido generado automáticamente.'}
${sectionId === 'PPT' ? 'RGPD y DNSH/PRTR incluidos.' : ''}
${sectionId === 'JN' ? 'Necesidad justificada sin fraccionamiento.' : ''}`
        
        setStepContent(sectionId, mockContent, [`${sectionId}_Ref_001`])
      }, sections.indexOf(sectionId) * 500)
    }

    setTimeout(() => {
      addMessage('bot', 'Se generaron JN, PPT, CEC y CR en orden. Valida y ajusta cada sección antes de exportar.')
    }, sections.length * 500)
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

  return (
    <aside className="lg:col-span-5 bg-white border border-gray-200 rounded-xl p-4 shadow-soft">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-base font-semibold">Orquestador de secciones</h2>
        <span className="text-xs text-muted">Orden: JN → PPT → CEC → CR</span>
      </div>
      
      <StepsList />
      
      <CompliancePanel />
      
      <CoherencePanel />
      
      <div className="mt-3 flex items-center gap-2">
        <button 
          onClick={handleGenerateAll}
          className="flex-1 px-3 py-2 rounded-lg cm-btn text-sm"
        >
          Generar todo
        </button>
        <button 
          onClick={() => setShowDraftModal(true)}
          className="px-3 py-2 rounded-lg border cm-outline text-sm"
        >
          Editar borrador
        </button>
      </div>
    </aside>
  )
}

export default AdminPanel
