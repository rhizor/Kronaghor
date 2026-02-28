import { useState } from 'react'
import { aiApi } from '../services/api'
import { useChatStore } from '../hooks/useStore'
import toast from 'react-hot-toast'

export default function ConsultorIA() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [provider, setProvider] = useState('openai')
  const { messages, addMessage, clear } = useChatStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    const userMessage = message
    addMessage('user', userMessage)
    setMessage('')
    setLoading(true)

    try {
      const { data } = await aiApi.chat(userMessage, provider)
      addMessage('assistant', data.response)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al enviar mensaje')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-slate-800">⚖️ Consultor IA Legal</h1>
        <div className="flex items-center gap-4">
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            className="px-3 py-2 bg-white border border-slate-300 rounded-lg"
          >
            <option value="openai">OpenAI (GPT-4)</option>
            <option value="grok">Grok</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
          <button
            onClick={clear}
            className="px-3 py-2 text-sm text-slate-600 hover:text-slate-800"
          >
            Limpiar Chat
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 bg-white rounded-xl shadow-sm p-4 overflow-y-auto mb-4">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-400">
            <div className="text-center">
              <p className="text-4xl mb-2">⚖️</p>
              <p>Haz tu primera consulta legal</p>
              <p className="text-sm mt-2">Ej: "¿Cuál es el término para responder una demanda?"</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-4 rounded-xl ${
                    msg.role === 'user'
                      ? 'bg-amber-500 text-white'
                      : 'bg-slate-100 text-slate-800'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-100 p-4 rounded-xl">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
                    <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></span>
                    <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Escribe tu consulta legal..."
          className="flex-1 px-4 py-3 bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !message.trim()}
          className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl disabled:opacity-50"
        >
          Enviar
        </button>
      </form>
    </div>
  )
}
