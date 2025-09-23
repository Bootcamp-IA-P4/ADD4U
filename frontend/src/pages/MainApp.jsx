import React from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useAppState } from '../contexts/AppStateContext'
import Header from '../components/Header'
import ContextSection from '../components/ContextSection'
import QuickActions from '../components/QuickActions'
import ChatSection from '../components/ChatSection'
import AdminPanel from '../components/AdminPanel'
import DraftModal from '../components/DraftModal'
import Toast from '../components/Toast'

const MainApp = () => {
  const { isAdmin } = useAuth()
  const { showDraftModal } = useAppState()

  return (
    <div className="min-h-screen bg-[#FAFAFA] text-ink">
      {/* Franja institucional */}
      <div className="w-full h-1.5" style={{background: 'var(--cm-red)'}}></div>

      <div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-5">
        <Header />

        {/* Top grid: Contexto + Sugerencias + Indicadores */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-4">
          <ContextSection />
          <QuickActions />
        </div>

        {/* Main grid: Chat + Orquestador */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
          <ChatSection />
          {isAdmin && <AdminPanel />}
        </div>
      </div>

      {/* Modales */}
      {showDraftModal && <DraftModal />}
      <Toast />
    </div>
  )
}

export default MainApp
