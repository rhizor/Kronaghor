import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './hooks/useStore'

// Pages
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ConsultorIA from './pages/ConsultorIA'
import Expedientes from './pages/Expedientes'
import Audiencias from './pages/Audiencias'
import LegalResearch from './pages/LegalResearch'

// Components
import Sidebar from './components/Sidebar'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50 flex">
      <Sidebar />
      <main className="flex-1 overflow-auto p-6">
        {children}
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/" element={
          <PrivateRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/consultor" element={
          <PrivateRoute>
            <Layout>
              <ConsultorIA />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/expedientes" element={
          <PrivateRoute>
            <Layout>
              <Expedientes />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/audiencias" element={
          <PrivateRoute>
            <Layout>
              <Audiencias />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/jurisprudencia" element={
          <PrivateRoute>
            <Layout>
              <LegalResearch />
            </Layout>
          </PrivateRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
