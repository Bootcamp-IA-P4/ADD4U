/**
 * Sistema de Re-pregunta Inteligente
 * Detecta información faltante y solicita aclaraciones
 */

const ClarificationPrompts = ({ userInput, onSendClarification }) => {
  // Análisis de información faltante
  const analyzeMissingInfo = (text) => {
    const missing = [];
    
    if (!text.match(/\d+\s*(unidades?|equipos?|metros?|kilómetros?)/i)) {
      missing.push({
        type: 'quantity',
        question: '¿Cuántas unidades o qué cantidad necesitas?',
        suggestions: ['10 unidades', '50 equipos', '100 metros cuadrados']
      });
    }
    
    if (!text.match(/(€|euros?|presupuesto|coste|precio)/i)) {
      missing.push({
        type: 'budget',
        question: '¿Tienes un presupuesto estimado?',
        suggestions: ['Sin presupuesto definido', 'Entre 10.000€ y 50.000€', 'Más de 100.000€']
      });
    }
    
    if (!text.match(/(plazo|fecha|mes|año|días?)/i)) {
      missing.push({
        type: 'timeline',
        question: '¿Cuál es el plazo de ejecución o entrega?',
        suggestions: ['1 mes', '3 meses', '6 meses', '1 año']
      });
    }
    
    if (!text.match(/(ubicación|lugar|edificio|dirección|municipio)/i)) {
      missing.push({
        type: 'location',
        question: '¿Dónde se realizará el servicio o entrega?',
        suggestions: ['Edificio central', 'Múltiples ubicaciones', 'Toda la provincia']
      });
    }
    
    if (!text.match(/(requisitos?|características?|especificaciones?|técnic)/i)) {
      missing.push({
        type: 'requirements',
        question: '¿Hay requisitos técnicos específicos?',
        suggestions: ['Sin requisitos especiales', 'Certificaciones necesarias', 'Normativa específica']
      });
    }
    
    return missing;
  };

  const missingInfo = analyzeMissingInfo(userInput);

  if (missingInfo.length === 0 || userInput.length < 20) {
    return null;
  }

  return (
    <div className="w-full bg-white border-2 border-brand-blue rounded-lg p-5 mb-4">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-10 h-10 bg-brand-blue flex items-center justify-center rounded">
          <span className="text-2xl font-bold text-white">?</span>
        </div>
        
        <div className="flex-1">
          <h4 className="text-sm font-bold text-brand-blue mb-2">
            Para mejorar tu documento, necesitamos más información:
          </h4>
          
          <div className="space-y-3">
            {missingInfo.slice(0, 2).map((item, idx) => (
              <div key={idx} className="bg-brand-beige border-2 border-gray-300 rounded-lg p-3">
                <p className="text-sm font-semibold text-ink mb-2">
                  {item.question}
                </p>
                <div className="flex flex-wrap gap-2">
                  {item.suggestions.map((suggestion, sidx) => (
                    <button
                      key={sidx}
                      onClick={() => onSendClarification(`${suggestion}`)}
                      className="text-xs px-3 py-2 bg-white hover:bg-brand-green hover:text-white text-ink font-medium rounded border-2 border-gray-300 hover:border-brand-green transition-all"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-3 flex items-center gap-2">
            <button
              onClick={() => onSendClarification('Continuar sin más información')}
              className="text-xs text-muted hover:text-brand-blue underline"
            >
              Continuar sin más información
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClarificationPrompts;
