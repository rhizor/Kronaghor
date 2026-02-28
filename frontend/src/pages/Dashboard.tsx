import { useEffect, useState } from 'react'
import { metricsApi } from '../services/api'
import { DashboardMetrics } from '../types'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMetrics()
  }, [])

  const loadMetrics = async () => {
    try {
      const { data } = await metricsApi.getDashboard()
      setMetrics(data)
    } catch (error) {
      console.error('Error loading metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500"></div>
      </div>
    )
  }

  const statCards = [
    { label: 'Total Expedientes', value: metrics?.total_expedientes || 0, icon: '📁', color: 'blue' },
    { label: 'Audiencias Próximas', value: metrics?.audiencias_proximas || 0, icon: '📅', color: 'green' },
    { label: 'Términos por Vencer', value: metrics?.terminos_por_vencer || 0, icon: '⏰', color: 'red' },
    { label: 'Nuevos (30 días)', value: metrics?.nuevos_30_dias || 0, icon: '✨', color: 'amber' },
  ]

  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
    amber: 'bg-amber-500',
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-6">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500">{card.label}</p>
                <p className="text-3xl font-bold text-slate-800 mt-1">{card.value}</p>
              </div>
              <div className={`w-12 h-12 ${colorClasses[card.color]} rounded-lg flex items-center justify-center text-2xl`}>
                {card.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Expedientes por Estado */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Expedientes por Estado</h2>
          <div className="space-y-3">
            {metrics?.por_estado && Object.entries(metrics.por_estado).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <span className="text-slate-600 capitalize">{status}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-amber-500 rounded-full"
                      style={{ width: `${(count / (metrics.total_expedientes || 1)) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium w-8">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Expedientes por Tipo</h2>
          <div className="space-y-3">
            {metrics?.por_tipo && Object.entries(metrics.por_tipo).map(([tipo, count]) => (
              <div key={tipo} className="flex items-center justify-between">
                <span className="text-slate-600 capitalize">{tipo}</span>
                <span className="text-sm font-medium px-2 py-1 bg-slate-100 rounded">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
