import React, { useState, useEffect } from 'react'

const Toast = () => {
  const [toasts, setToasts] = useState([])

  useEffect(() => {
    // Listen for global toast events
    const handleToast = (event) => {
      const { message, type = 'info', duration = 3000 } = event.detail
      const id = Date.now()
      
      setToasts(prev => [...prev, { id, message, type }])
      
      setTimeout(() => {
        setToasts(prev => prev.filter(toast => toast.id !== id))
      }, duration)
    }

    window.addEventListener('showToast', handleToast)
    return () => window.removeEventListener('showToast', handleToast)
  }, [])

  const removeToast = (id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }

  const getToastStyles = (type) => {
    switch (type) {
      case 'success':
        return 'bg-emerald-50 border-emerald-200 text-emerald-800'
      case 'error':
        return 'bg-red-50 border-red-200 text-red-800'
      case 'warning':
        return 'bg-amber-50 border-amber-200 text-amber-800'
      default:
        return 'bg-white border-gray-200 text-ink'
    }
  }

  if (toasts.length === 0) return null

  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`px-4 py-2 rounded-lg shadow-soft border animate-slide-in ${getToastStyles(toast.type)}`}
          style={{ 
            animation: 'slideIn 0.3s ease-out',
            maxWidth: '300px'
          }}
        >
          <div className="flex items-center justify-between">
            <span className="text-sm">{toast.message}</span>
            <button
              onClick={() => removeToast(toast.id)}
              className="ml-2 text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

// Global function to show toasts
export const showToast = (message, type = 'info', duration = 3000) => {
  const event = new CustomEvent('showToast', {
    detail: { message, type, duration }
  })
  window.dispatchEvent(event)
}

export default Toast
