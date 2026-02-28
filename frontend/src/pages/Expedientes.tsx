import { useState, useEffect } from 'react'
import { expApi } from '../services/api'
import { Expediente } from '../types'
import toast from 'react-hot-toast'

const tipos = ['civil', 'penal', 'laboral', 'contencioso', 'administrativo', 'familia', 'otro']

export default function Expedientes() {
  const [expedientes, setExpedientes] = useState<Expediente[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    numero: '',
    tipo: 'civil',
    demandante: '',
    demandado: '',
    objeto: '',
    valor: '',
    notas: ''
  })

  useEffect(() => {
    loadExpedientes()
  }, [])

  const loadExpedientes = async () => {
    try {
      const { data } = await expApi.list()
      setExpedientes(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await expApi.create({
        ...formData,
        valor: formData.valor ? parseFloat(formData.valor) : null
      })
      toast.success('Expediente creado')
      setShowForm(false)
      setFormData({ numero: '', tipo: 'civil', demandante: '', demandado: '', objeto: '', valor: '', notas: '' })
      loadExpedientes()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al crear')
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('¿Eliminar expediente?')) return
    try {
      await expApi.delete(id)
      toast.success('Eliminado')
      loadExpedientes()
    } catch (error) {
      toast.error('Error al eliminar')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-800">📁 Expedientes</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white font-medium rounded-lg"
        >
          {showForm ? 'Cancelar' : '+ Nuevo Expediente'}
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl p-6 mb-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Número *</label>
              <input
                type="text"
                value={formData.numero}
                onChange={(e) => setFormData({ ...formData, numero: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Tipo</label>
              <select
                value={formData.tipo}
                onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              >
                {tipos.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Demandante</label>
              <input
                type="text"
                value={formData.demandante}
                onChange={(e) => setFormData({ ...formData, demandante: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Demandado</label>
              <input
                type="text"
                value={formData.demandado}
                onChange={(e) => setFormData({ ...formData, demandado: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-1">Objeto</label>
              <input
                type="text"
                value={formData.objeto}
                onChange={(e) => setFormData({ ...formData, objeto: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Valor</label>
              <input
                type="number"
                value={formData.valor}
                onChange={(e) => setFormData({ ...formData, valor: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              />
            </div>
          </div>
          <button type="submit" className="mt-4 px-4 py-2 bg-amber-500 text-white rounded-lg">
            Crear Expediente
          </button>
        </form>
      )}

      {/* List */}
      {loading ? (
        <div className="text-center py-8 text-slate-400">Cargando...</div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Número</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Tipo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Demandante</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Demandado</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Estado</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-slate-600">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {expedientes.map((exp) => (
                <tr key={exp.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium">{exp.numero}</td>
                  <td className="px-4 py-3 capitalize">{exp.tipo}</td>
                  <td className="px-4 py-3">{exp.demandante || '-'}</td>
                  <td className="px-4 py-3">{exp.demandado || '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      exp.status === 'activo' ? 'bg-green-100 text-green-700' :
                      exp.status === 'cerrado' ? 'bg-blue-100 text-blue-700' :
                      'bg-slate-100 text-slate-700'
                    }`}>
                      {exp.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDelete(exp.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
              {expedientes.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-slate-400">
                    No hay expedientes
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
