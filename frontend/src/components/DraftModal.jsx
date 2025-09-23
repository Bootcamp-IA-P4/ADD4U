import React, { useEffect, useRef } from 'react'
import { useAppState } from '../contexts/AppStateContext'

const DraftModal = () => {
  const { 
    draft, 
    setShowDraftModal, 
    updateDraftSection, 
    removeDraftSection, 
    clearDraft,
    wordCount 
  } = useAppState()
  const modalRef = useRef(null)

  const handleClose = () => {
    setShowDraftModal(false)
  }

  const handleBackdropClick = (e) => {
    if (e.target === modalRef.current) {
      handleClose()
    }
  }

  const handleDownload = () => {
    const content = buildMarkdown()
    downloadFile('expediente.md', content, 'text/markdown;charset=utf-8')
  }

  const buildMarkdown = () => {
    const ctx = `# Propuesta — Proceso

- Entidad: —
- Fecha límite: —

---`
    
    const body = Object.entries(draft.sections || {}).map(([k, v]) => `## ${k}\n${v}`).join('\n\n')
    return `${ctx}\n\n${body || '_(sin contenido)_'}`
  }

  const downloadFile = (filename, content, mimeType = 'text/markdown;charset=utf-8') => {
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.rel = 'noopener noreferrer'
    a.target = '_blank'
    document.body.appendChild(a)
    a.click()
    setTimeout(() => {
      URL.revokeObjectURL(url)
      document.body.removeChild(a)
    }, 200)
  }

  const getTotalWords = () => {
    return Object.values(draft.sections || {}).reduce((total, content) => {
      return total + wordCount(content)
    }, 0)
  }

  const sectionKeys = Object.keys(draft.sections || {})

  return (
    <div 
      ref={modalRef}
      onClick={handleBackdropClick}
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div className="absolute inset-0 bg-black/30"></div>
      <div className="relative w-full max-w-3xl bg-white rounded-xl p-4 border border-gray-200 shadow-soft">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold">Borrador del expediente</h3>
          <button 
            onClick={handleClose}
            className="px-2 py-1 rounded-lg border cm-outline text-sm"
          >
            ✕
          </button>
        </div>
        
        <div className="space-y-3 max-h-[65vh] overflow-y-auto scrollbar">
          {sectionKeys.length === 0 ? (
            <div className="text-sm text-muted">
              Aún no hay secciones. Genera y "Añadir al borrador".
            </div>
          ) : (
            sectionKeys.map(sectionName => (
              <div key={sectionName} className="rounded-lg border border-gray-200 bg-white p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm font-medium">
                    {sectionName} 
                    <span className="text-xs text-muted ml-2">
                      ({wordCount(draft.sections[sectionName])} palabras)
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={() => removeDraftSection(sectionName)}
                      className="px-2 py-1 rounded-md border cm-outline text-xs"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
                <textarea
                  rows="5"
                  value={draft.sections[sectionName]}
                  onChange={(e) => updateDraftSection(sectionName, e.target.value)}
                  className="form-textarea"
                />
              </div>
            ))
          )}
        </div>
        
        <div className="mt-3 flex items-center justify-between gap-2">
          <div className="text-xs text-muted">
            Palabras totales: {getTotalWords()}
          </div>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => clearDraft()}
              className="px-3 py-2 rounded-lg border cm-outline text-sm"
            >
              Vaciar
            </button>
            <button 
              onClick={handleDownload}
              className="px-3 py-2 rounded-lg cm-btn text-sm"
            >
              Descargar .md
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DraftModal
