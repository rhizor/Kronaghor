import { useState, useEffect } from 'react'
import { audApi, expApi } from '../services/api'
import { Audiencia, Expediente } from '../types'
import toast from 'react-hot-toast'

const tipos = ['verbal', 'escrita', 'juicio', 'conciliación', 'inspección']

export default function Audiencias() {
  const [audiencias, setAudiencias] = useState<Audiencia[]>([])
  const [expedientes, setExpedientes] = useState<Expediente[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    expediente_id: 0,
    tipo: 'verbal',
    fecha: '',
    duracion_minutos: 60,
    lugar: '',
    notas: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [audRes, expRes] = await Promise.all([
        audApi.list(),
        expApi.list()
      ])
      setAudiencias(audRes.data)
      setExpedientes(expRes.data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await audApi.create({
        ...formData,
        expediente_id: parseInt(formData.expediente_id as any),
        fecha: new Date(formData.fecha).toISOString()
      })
      toast.success('Audiencia creada')
      setShowForm(false)
      setFormData({ expediente_id: 0, tipo: 'verbal', fecha: '', duracion_minutos: 60, lugar: '', notas: '' })
      loadData()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al crear')
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('¿Eliminar audiencia?')) return
    try {
      await audApi.delete(id)
      toast.success('Eliminada')
      loadData()
    } catch (error) {
      toast.error('Error al eliminar')
    }
  }

  const getExpedienteNumero = (id: number) => {
    const exp = expedientes.find(e => e.id === id)
    return exp?.numero || '#' + id
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-800">📅 Audiencias</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white font-medium rounded-lg"
        >
          {showForm ? 'Cancelar' : '+ Nueva Audiencia'}
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl p-6 mb-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Expediente *</label>
              <select
                value={formData.expediente_id}
                onChange={(e) => setFormData({ ...formData, expediente_id: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
                required
              >
                <option value={0}>Seleccionar...</option>
                {expedientes.map(exp => (
                  <option key={exp.id} value={exp.id}>{exp.numero}</option>
                ))}
              </select>
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
              <label className="block text-sm font-medium text-slate-700 mb-1">Fecha *</label>
              <input
                type="datetime-local"
                value={formData.fecha}
                onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Duración (min)</label>
              <input
                type="number"
                value={formData.duracion_minutos}
                onChange={(e) => setFormData({ ...formData, duracion_minutos: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Lugar</label>
              <input
                type="text"
                value={formData.lugar}
                onChange={(e) => setFormData({ ...formData, lugar: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg"
              />
            </div>
          </div>
          <button type="submit" className="mt-4 px-4 py-2 bg-amber-500 text-white rounded-lg">
            Crear Audiencia
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
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Expediente</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Tipo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Fecha</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Lugar</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-600">Estado</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-slate-600">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {audiencias.map((aud) => (
                <tr key={aud.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium">{getExpedienteNumero(aud.expediente_id)}</td>
                  <td className="px-4 py-3 capitalize">{aud.tipo}</td>
                  <td className="px-4 py-3">{new Date(aud.fecha).toLocaleString()}</td>
                  <td className="px-4 py-3">{aud.lugar || '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      aud.status === 'programada' ? 'bg-green-100 text-green-700' :
                      aud.status === 'realizada' ? 'bg-blue-100 text-blue-700' :
                      'bg-slate-100 text-slate-700'
                    }`}>
                      {aud.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDelete(aud.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
              {audiencias.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-slate-400">
                    No hay audiencias
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
