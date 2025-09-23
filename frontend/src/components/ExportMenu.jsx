import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'

const ExportMenu = () => {
  const [showMenu, setShowMenu] = useState(false)
  const { isAdmin } = useAuth()

  const handleExport = (type) => {
    setShowMenu(false)
    
    switch (type) {
      case 'md':
        if (!isAdmin) {
          showToast('Solo Admin puede exportar expediente')
          return
        }
        downloadMarkdown()
        break
      case 'doc':
        if (!isAdmin) {
          showToast('Solo Admin puede exportar expediente')
          return
        }
        downloadDoc()
        break
      case 'json':
        if (!isAdmin) {
          showToast('Solo Admin puede exportar manifiesto')
          return
        }
        downloadManifest()
        break
      case 'chat':
        downloadChat()
        break
    }
  }

  const downloadMarkdown = () => {
    const content = buildMarkdown()
    downloadFile('expediente.md', content, 'text/markdown;charset=utf-8')
  }

  const downloadDoc = () => {
    const content = contentToDoc(buildMarkdown())
    downloadFile('expediente.doc', content, 'application/msword')
  }

  const downloadManifest = () => {
    const content = buildManifest()
    downloadFile('manifest.json', content, 'application/json;charset=utf-8')
  }

  const downloadChat = () => {
    const content = exportChat()
    downloadFile('chat.txt', content, 'text/plain;charset=utf-8')
  }

  const buildMarkdown = () => {
    // Get draft sections from localStorage or context
    const draft = JSON.parse(localStorage.getItem('mini_celia_poc') || '{}')?.draft?.sections || {}
    
    const ctx = `# Propuesta — Proceso

- Entidad: —
- Fecha límite: —

---`
    
    const body = Object.entries(draft).map(([k, v]) => `## ${k}\n${v}`).join('\n\n')
    return `${ctx}\n\n${body || '_(sin contenido)_'}`
  }

  const contentToDoc = (markdownContent) => {
    const lines = (markdownContent || '').split('\n').map(l => {
      if (l.startsWith('### ')) return `<h3>${l.slice(4)}</h3>`
      if (l.startsWith('## ')) return `<h2>${l.slice(3)}</h2>`
      if (l.startsWith('# ')) return `<h1>${l.slice(2)}</h1>`
      if (l.startsWith('- ') || l.startsWith('• ')) return `<li>${l.replace(/^[-•]\s*/, '')}</li>`
      if (l.trim() === '') return '<br/>'
      return `<p>${l}</p>`
    }).join('\n').replace(/(<li>.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`)
    
    return `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>${lines}</body></html>`
  }

  const buildManifest = () => {
    const ts = new Date().toISOString()
    const manifest = {
      name: "Mini-CELIA PoC",
      generatedAt: ts,
      context: { proceso: '', entidad: '', fecha: '' },
      sections: [],
      compliance: { DNSH: false, PRTR: false, RGPD: false, Fracc: false, Missing: [] },
      coherence: { checked: false, ok: false, notes: [] },
      promptsVersion: "v0.1-canon",
      goldenRepoHash: "sim-hash-abc123"
    }
    return JSON.stringify(manifest, null, 2)
  }

  const exportChat = () => {
    // Get chat messages from DOM or context
    const chatMessages = Array.from(document.querySelectorAll('#chatBox > div')).map(node => {
      const isBot = node.querySelector('.bot-bubble') !== null
      const text = node.textContent.replace(/\s+\n/g, ' ').trim()
      return `${isBot ? 'Asesor' : 'Tú'}: ${text}`
    })
    return chatMessages.join('\n\n')
  }

  const downloadFile = (filename, content, mimeType = 'text/plain;charset=utf-8') => {
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

  // Close menu when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (e) => {
      if (showMenu && !e.target.closest('.export-menu-container')) {
        setShowMenu(false)
      }
    }

    document.addEventListener('click', handleClickOutside)
    return () => document.removeEventListener('click', handleClickOutside)
  }, [showMenu])

  return (
    <div className="relative export-menu-container">
      <button 
        onClick={() => setShowMenu(!showMenu)}
        className="px-3 py-2 rounded-lg cm-btn text-sm font-medium"
      >
        Exportar
      </button>
      
      {showMenu && (
        <div className="absolute right-0 mt-2 w-72 bg-white rounded-lg p-2 border border-gray-200 shadow-soft z-20">
          <button 
            onClick={() => handleExport('md')}
            className={`w-full text-left px-3 py-2 rounded-md hover:bg-gray-50 text-sm ${!isAdmin ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            Bajar expediente (.md)
          </button>
          <button 
            onClick={() => handleExport('doc')}
            className={`w-full text-left px-3 py-2 rounded-md hover:bg-gray-50 text-sm ${!isAdmin ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            Bajar expediente (.doc)
          </button>
          <button 
            onClick={() => handleExport('json')}
            className={`w-full text-left px-3 py-2 rounded-md hover:bg-gray-50 text-sm ${!isAdmin ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            Bajar manifiesto (.json)
          </button>
          <button 
            onClick={() => handleExport('chat')}
            className="w-full text-left px-3 py-2 rounded-md hover:bg-gray-50 text-sm"
          >
            Bajar chat (.txt)
          </button>
        </div>
      )}
    </div>
  )
}

export default ExportMenu
