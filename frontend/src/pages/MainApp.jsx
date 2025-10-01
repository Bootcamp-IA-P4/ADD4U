import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import Header from '../components/Header'
import ChatSection from '../components/ChatSection'
import DraftModal from '../components/DraftModal'
import Toast from '../components/Toast'

const MainApp = () => {
  const { showDraftModal } = useAppState()

  return (
    <div className="min-h-screen text-ink" style={{background: 'var(--gradient-bg)'}}>
      {/* Franja institucional con gradiente */}
      <div 
        className="w-full h-2" 
        style={{background: 'linear-gradient(90deg, var(--cm-red) 0%, var(--cm-red-dark) 100%)'}}
      ></div>      {/* Header con efecto glass centrado */}
      <div className="header-glass sticky top-0 z-10">
        <div className="px-4 md:px-6 lg:px-8 py-5">
          <Header />
        </div>
      </div>      {/* Contenido principal centrado */}
      <div className="flex items-center justify-center min-h-[calc(100vh-140px)] px-4 py-6">
        <div className="w-full max-w-5xl">
          {/* Descripción sutil */}
          <div className="text-center mb-6">
            <p className="text-lg text-muted max-w-3xl mx-auto font-medium">
              Generación automática e inteligente de documentos de licitación con validación normativa
            </p>
          </div>

          {/* Chat principal */}
          <div className="chat-container rounded-3xl p-6 md:p-8 float-animation">
            <ChatSection />
          </div>
        </div>
      </div>

      {/* Modales */}
      {showDraftModal && <DraftModal />}
      <Toast />
    </div>
  )
}

export default MainApp
