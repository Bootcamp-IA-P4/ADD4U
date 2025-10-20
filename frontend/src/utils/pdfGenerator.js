import jsPDF from 'jspdf'

/**
 * Genera un PDF profesional con todas las secciones JN disponibles (JN.1 a JN.5)
 * @param {string} expedienteId - ID del expediente (ej: "OBR-1234", "SER-5678")
 * @param {Array} sections - Array de objetos {id, title, content} para cada sección JN
 */
export const generateJNPDF = (expedienteId, sections) => {
  // Si se recibe un string en lugar de array (compatibilidad hacia atrás)
  if (typeof sections === 'string') {
    sections = [{
      id: 'JN.1',
      title: 'Justificación de la Necesidad',
      content: sections
    }]
  }
  const doc = new jsPDF()
  
  // Configuración inicial
  const pageWidth = doc.internal.pageSize.getWidth()
  const pageHeight = doc.internal.pageSize.getHeight()
  const margin = 20
  const maxWidth = pageWidth - (margin * 2)
  let yPosition = margin
  
  // Helper para limpiar texto HTML
  const cleanText = (text) => {
    return text
      .replace(/<[^>]*>/g, '') // Eliminar tags HTML
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/\s+/g, ' ') // Normalizar espacios
      .trim()
  }
  
  // Helper para añadir nueva página si es necesario
  const checkPageBreak = (requiredSpace = 20) => {
    if (yPosition + requiredSpace > pageHeight - margin) {
      doc.addPage()
      yPosition = margin
      return true
    }
    return false
  }
  
  // Helper para texto con wrap y justificación mejorada
  const addWrappedText = (text, fontSize, isBold = false) => {
    doc.setFontSize(fontSize)
    doc.setFont('helvetica', isBold ? 'bold' : 'normal')
    
    // Dividir por párrafos primero
    const paragraphs = text.split(/\n\n+|\r\n\r\n+/)
    
    paragraphs.forEach((paragraph, index) => {
      if (!paragraph.trim()) return
      
      const lines = doc.splitTextToSize(paragraph.trim(), maxWidth)
      lines.forEach((line, lineIndex) => {
        checkPageBreak(fontSize * 0.7)
        doc.text(line, margin, yPosition)
        yPosition += fontSize * 0.5
      })
      
      // Espacio entre párrafos (excepto el último)
      if (index < paragraphs.length - 1) {
        yPosition += 4
      }
    })
    
    yPosition += 3
  }
  
  // Header del PDF - Azul corporativo
  doc.setFillColor(41, 128, 185) // Azul Mini-CELIA
  doc.rect(0, 0, pageWidth, 35, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(22)
  doc.setFont('helvetica', 'bold')
  doc.text('Mini-CELIA', margin, 22)
  
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.text('Copilot Inteligente de Licitaciones', margin, 28)
  
  yPosition = 50
  
  // Información del expediente - Caja destacada
  doc.setFillColor(240, 240, 240)
  doc.rect(margin, yPosition, maxWidth, 25, 'F')
  
  doc.setTextColor(0, 0, 0)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text(`Expediente: ${expedienteId || 'SIN_ID'}`, margin + 5, yPosition + 8)
  
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  const sectionsList = sections.map(s => s.id).join(', ')
  doc.text(`Secciones: ${sectionsList}`, margin + 5, yPosition + 16)
  
  yPosition += 35
  
  // Fecha de generación
  const fecha = new Date().toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
  doc.setFontSize(9)
  doc.setFont('helvetica', 'italic')
  doc.setTextColor(120, 120, 120)
  doc.text(`Documento generado el: ${fecha}`, margin, yPosition)
  yPosition += 8
  
  // Línea separadora elegante
  doc.setDrawColor(41, 128, 185)
  doc.setLineWidth(0.5)
  doc.line(margin, yPosition, pageWidth - margin, yPosition)
  yPosition += 15
  
  // Renderizar cada sección JN
  sections.forEach((section, index) => {
    // Verificar si necesitamos nueva página para el título
    checkPageBreak(30)
    
    // Título de la sección
    doc.setTextColor(41, 128, 185)
    doc.setFontSize(13)
    doc.setFont('helvetica', 'bold')
    doc.text(`${section.id} - ${section.title}`, margin, yPosition)
    yPosition += 10
    
    // Contenido de la sección
    doc.setTextColor(40, 40, 40)
    const cleanContent = cleanText(section.content)
    
    if (cleanContent && cleanContent.length > 50) {
      addWrappedText(cleanContent, 10.5, false)
    } else {
      doc.setTextColor(150, 150, 150)
      doc.setFont('helvetica', 'italic')
      addWrappedText('No hay contenido generado para esta sección.', 10, false)
    }
    
    // Espacio entre secciones (excepto la última)
    if (index < sections.length - 1) {
      yPosition += 10
      checkPageBreak(20)
      
      // Línea separadora sutil entre secciones
      doc.setDrawColor(200, 200, 200)
      doc.setLineWidth(0.3)
      doc.line(margin + 30, yPosition, pageWidth - margin - 30, yPosition)
      yPosition += 15
    }
  })
  
  // Footer en todas las páginas
  const totalPages = doc.internal.getNumberOfPages()
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i)
    
    // Línea superior del footer
    doc.setDrawColor(200, 200, 200)
    doc.setLineWidth(0.3)
    doc.line(margin, pageHeight - 20, pageWidth - margin, pageHeight - 20)
    
    // Texto del footer
    doc.setFontSize(8)
    doc.setTextColor(120, 120, 120)
    doc.setFont('helvetica', 'normal')
    
    // Izquierda: Expediente
    doc.text(`${expedienteId || 'JN1'}`, margin, pageHeight - 12)
    
    // Centro: Mini-CELIA
    doc.text(
      'Generado por Mini-CELIA',
      pageWidth / 2,
      pageHeight - 12,
      { align: 'center' }
    )
    
    // Derecha: Número de página
    doc.text(
      `Pág. ${i}/${totalPages}`,
      pageWidth - margin,
      pageHeight - 12,
      { align: 'right' }
    )
  }
  
  // Descargar el PDF con nombre descriptivo
  const timestamp = new Date().toISOString().split('T')[0]
  const fileName = `${expedienteId || 'JN1'}_${timestamp}.pdf`
  doc.save(fileName)
  
  return fileName
}