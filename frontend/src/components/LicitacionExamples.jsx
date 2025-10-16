/**
 * Ejemplos de Licitación por Categoría
 * Facilita el inicio de conversa      <h3 className="text-lg font-bold text-brand-blue mb-2">
        Ejemplos de Licitación por Categoría
      </h3>nes con plantillas predefinidas
 */

const LicitacionExamples = ({ onSelectExample }) => {
  const examples = [
    {
      category: 'Servicios',
      icon: '',
      color: 'brand-blue',
      examples: [
        {
          title: 'Servicios de Limpieza',
          text: 'Necesitamos contratar servicios de limpieza para 5 edificios municipales con una frecuencia diaria. El contrato debe incluir suministro de material de limpieza y personal cualificado.',
          tooltip: 'Ejemplo de licitación de servicios de limpieza para edificios públicos'
        },
        {
          title: 'Mantenimiento Informático',
          text: 'Requerimos mantenimiento y soporte técnico informático para 200 equipos distribuidos en diferentes departamentos. Incluye actualizaciones, reparaciones y soporte remoto.',
          tooltip: 'Ejemplo de contrato de mantenimiento IT'
        }
      ]
    },
    {
      category: 'Obras',
      icon: '',
      color: 'brand-yellow',
      examples: [
        {
          title: 'Rehabilitación de Edificio',
          text: 'Proyecto de rehabilitación integral de edificio histórico municipal de 1500m². Incluye restauración de fachada, mejora de accesibilidad y actualización de instalaciones.',
          tooltip: 'Ejemplo de obra pública de rehabilitación'
        },
        {
          title: 'Pavimentación Urbana',
          text: 'Obras de pavimentación y mejora de 3 calles del casco urbano, con una longitud total de 800 metros lineales. Incluye renovación de aceras y mejora del alumbrado.',
          tooltip: 'Ejemplo de obra de urbanización'
        }
      ]
    },
    {
      category: 'Suministros',
      icon: '',
      color: 'brand-green',
      examples: [
        {
          title: 'Equipos Informáticos',
          text: 'Suministro de 50 ordenadores portátiles y 20 equipos de sobremesa para renovación del parque informático municipal. Características técnicas mínimas: i5, 16GB RAM, SSD 512GB.',
          tooltip: 'Ejemplo de suministro de equipamiento tecnológico'
        },
        {
          title: 'Mobiliario de Oficina',
          text: 'Adquisición de mobiliario de oficina para nuevas dependencias: 30 mesas de trabajo, 50 sillas ergonómicas, 15 armarios archivadores y 10 mesas de reuniones.',
          tooltip: 'Ejemplo de suministro de mobiliario'
        }
      ]
    },
    {
      category: 'Consultoría',
      icon: '',
      color: 'brand-blue',
      examples: [
        {
          title: 'Auditoría Energética',
          text: 'Contratación de servicios de consultoría para realizar auditoría energética de 10 edificios municipales, incluyendo propuestas de mejora y plan de ahorro energético.',
          tooltip: 'Ejemplo de consultoría especializada'
        },
        {
          title: 'Asesoría Legal',
          text: 'Servicios de asesoramiento jurídico especializado en contratación pública para el departamento de compras, con disponibilidad de 20 horas mensuales durante 12 meses.',
          tooltip: 'Ejemplo de servicio de asesoría'
        }
      ]
    }
  ];

  return (
    <div className="w-full bg-white border-2 border-gray-300 rounded-lg p-6 mb-6 shadow-sm">
      <h3 className="text-lg font-bold text-brand-blue mb-2 flex items-center gap-2">
        � Ejemplos de Licitación por Categoría
      </h3>
      <p className="text-sm text-muted mb-6">
        Selecciona un ejemplo para comenzar
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {examples.map((category) => (
          <div key={category.category} className="border-2 border-gray-300 rounded-lg p-4 bg-brand-beige">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-2xl">{category.icon}</span>
              <h4 className="font-bold text-ink">
                {category.category}
              </h4>
            </div>

            <div className="space-y-2">
              {category.examples.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => onSelectExample(example.text)}
                  className="w-full text-left p-3 bg-white border-2 border-gray-300 hover:border-brand-green rounded-lg transition-all group"
                  title={example.tooltip}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 flex items-start gap-2">

                      <div>
                        <p className="text-sm font-semibold text-ink">
                          {example.title}
                        </p>
                        <p className="text-xs text-muted mt-1 line-clamp-2">
                          {example.text}
                        </p>
                      </div>
                    </div>
                    <svg
                      className="w-4 h-4 text-muted group-hover:text-brand-green transition-colors flex-shrink-0 ml-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 p-4 bg-brand-yellow border-2 border-gray-300 rounded-lg">
        <p className="text-sm font-semibold text-ink">
          <strong>Consejo:</strong> Cuanta más información proporciones (cantidades, ubicación, requisitos técnicos, plazos), mejor será el documento generado.
        </p>
      </div>
    </div>
  );
};

export default LicitacionExamples;

