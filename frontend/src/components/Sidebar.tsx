import { Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../hooks/useStore'

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/consultor', label: 'Consultor IA', icon: '⚖️' },
  { path: '/expedientes', label: 'Expedientes', icon: '📁' },
  { path: '/audiencias', label: 'Audiencias', icon: '📅' },
  { path: '/jurisprudencia', label: 'Jurisprudencia', icon: '📚' },
]

export default function Sidebar() {
  const location = useLocation()
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-amber-500 rounded-lg flex items-center justify-center">
            <span className="text-xl font-bold">K</span>
          </div>
          <div>
            <h1 className="font-bold">Kronaghor</h1>
            <p className="text-xs text-slate-400">Asistente Jurídico</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-amber-600 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* User */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center justify-between">
          <div className="text-sm">
            <p className="font-medium">{user?.username || 'Usuario'}</p>
            <p className="text-xs text-slate-400">{user?.role || 'user'}</p>
          </div>
          <button
            onClick={logout}
            className="text-sm text-slate-400 hover:text-white"
          >
            Salir
          </button>
        </div>
      </div>
    </aside>
  )
}
