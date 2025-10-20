
import React from 'react'
import { useAppState } from '../contexts/AppStateContext'
import ChatSection from '../components/ChatSection'
import DraftModal from '../components/DraftModal'
import Toast from '../components/Toast'

const MainApp = () => {
  const { showDraftModal } = useAppState()

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{background: '#f8f4eb'}}>
      {/* Chat principal - ocupa toda la pantalla */}
      <div className="w-full max-w-6xl h-[95vh]">
        <div className="bg-brand-yellow rounded-3xl shadow-lg h-full overflow-hidden">
          <ChatSection />
        </div>
      </div>

      {/* Modales */}
      {showDraftModal && <DraftModal />}
      <Toast />
    </div>
  )
}

export default MainApp
