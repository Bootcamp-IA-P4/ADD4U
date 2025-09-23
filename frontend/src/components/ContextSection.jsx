import React from 'react'
import { useAppState } from '../contexts/AppStateContext'

const ContextSection = () => {
  const { state, updateContext, getContextCompletion } = useAppState()
  const { filled, total } = getContextCompletion()

  const handleInputChange = (field, value) => {
    updateContext(field, value)
  }

  return (
    <section className="lg:col-span-6 bg-white border border-gray-200 rounded-xl p-4 shadow-soft">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-base font-semibold">Contexto del proceso</h2>
        <span 
          className={`text-xs px-2.5 py-1 rounded-full border ${
            filled === total 
              ? 'border-emerald-300 text-emerald-700 bg-emerald-50' 
              : 'border-gray-300 text-muted'
          }`}
        >
          {filled === total ? 'Completo' : `Incompleto (${filled}/${total})`}
        </span>
      </div>
      
      <form className="grid sm:grid-cols-3 gap-3">
        <div>
          <label className="block text-sm mb-1" htmlFor="proceso">Proceso</label>
          <input
            id="proceso"
            value={state.ctx.proceso}
            onChange={(e) => handleInputChange('proceso', e.target.value)}
            className="form-input"
            placeholder="Ej: Mantenimiento integral"
          />
        </div>
        
        <div>
          <label className="block text-sm mb-1" htmlFor="entidad">Entidad</label>
          <input
            id="entidad"
            value={state.ctx.entidad}
            onChange={(e) => handleInputChange('entidad', e.target.value)}
            className="form-input"
            placeholder="Ej: Comunidad de..."
          />
        </div>
        
        <div>
          <label className="block text-sm mb-1" htmlFor="fecha">Fecha límite</label>
          <input
            id="fecha"
            type="date"
            value={state.ctx.fecha}
            onChange={(e) => handleInputChange('fecha', e.target.value)}
            className="form-input"
          />
        </div>
      </form>
      
      <p className="mt-2 text-xs text-muted">
        La IU funciona por "slots": completa solo lo necesario, el resto se preguntará en el chat.
      </p>
    </section>
  )
}

export default ContextSection
