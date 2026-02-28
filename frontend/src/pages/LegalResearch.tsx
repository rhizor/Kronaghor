import { useState } from 'react'

// This would connect to jurisprudencia APIs in production
export default function LegalResearch() {
  const [search, setSearch] = useState('')
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!search.trim()) return

    setLoading(true)
    
    // Simulated results for demo
    // In production, this would call: jurisprudence APIs, secretaría, etc.
    setTimeout(() => {
      setResults([
        {
          tipo: 'Corte Constitucional',
          fecha: '2024-01-15',
          referencia: 'C-123/24',
          objeto: 'Demanda de inconstitucionalidad contra...',
          demandante: 'Ciudadano X',
          demandado: 'Presidente de la República',
          url: '#'
        },
        {
          tipo: 'Consejo de Estado',
          fecha: '2024-01-10',
          referencia: 'SC-456/24',
          objeto: 'Nulidad electoral...',
          demandante: 'Partido político Y',
          demandado: 'Registraduría',
          url: '#'
        }
      ])
      setLoading(false)
    }, 1000)
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-6">📚 Explorador de Jurisprudencia</h1>

      {/* Search */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por número, demandante, demandado, objeto..."
            className="flex-1 px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-lg disabled:opacity-50"
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </button>
        </div>
      </form>

      {/* Filters */}
      <div className="flex gap-2 mb-6">
        <select className="px-3 py-2 bg-white border border-slate-300 rounded-lg">
          <option>Todas las cortes</option>
          <option>Corte Constitucional</option>
          <option>Corte Suprema</option>
          <option>Consejo de Estado</option>
        </select>
        <select className="px-3 py-2 bg-white border border-slate-300 rounded-lg">
          <option>Todos los años</option>
          <option>2024</option>
          <option>2023</option>
          <option>2022</option>
        </select>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {results.length === 0 && !loading && (
          <div className="text-center py-12 text-slate-400">
            <p className="text-4xl mb-4">📚</p>
            <p>Ingresa un término de búsqueda</p>
          </div>
        )}

        {results.map((result, idx) => (
          <div key={idx} className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">
                    {result.tipo}
                  </span>
                  <span className="text-sm text-slate-500">{result.fecha}</span>
                </div>
                <h3 className="font-bold text-lg text-slate-800">{result.referencia}</h3>
              </div>
              <a href={result.url} className="text-amber-600 hover:underline">
                Ver →
              </a>
            </div>
            
            <p className="text-slate-600 mt-2">{result.objeto}</p>
            
            <div className="mt-3 flex gap-4 text-sm text-slate-500">
              <span>Demandante: <strong>{result.demandante}</strong></span>
              <span>Demandado: <strong>{result.demandado}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
