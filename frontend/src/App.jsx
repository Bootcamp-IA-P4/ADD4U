import React from 'react'
import { AppStateProvider } from './contexts/AppStateContext'
import MainApp from './pages/MainApp'

function App() {
  return (
    <AppStateProvider>
      <MainApp />
    </AppStateProvider>
  )
}

export default App
