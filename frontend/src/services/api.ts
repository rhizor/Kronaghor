import axios from 'axios'

const API_URL = '/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }),
  
  register: (email: string, username: string, password: string, fullName?: string) =>
    api.post('/auth/register', { email, username, password, full_name: fullName }),
  
  me: () => api.get('/auth/me')
}

// AI
export const aiApi = {
  chat: (message: string, provider?: string, model?: string) =>
    api.post('/ai/chat', { message, provider, model }),
  
  getProviders: () => api.get('/ai/providers'),
  
  getHistory: (limit?: number) => api.get('/ai/chat/history', { params: { limit } }),
  
  clearHistory: () => api.delete('/ai/chat/history')
}

// Expedientes
export const expApi = {
  list: (params?: { status?: string; tipo?: string; search?: string }) =>
    api.get('/expedientes', { params }),
  
  get: (id: number) => api.get(`/expedientes/${id}`),
  
  create: (data: any) => api.post('/expedientes', data),
  
  update: (id: number, data: any) => api.put(`/expedientes/${id}`, data),
  
  delete: (id: number) => api.delete(`/expedientes/${id}`),
  
  uploadDocument: (id: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/expedientes/${id}/documentos`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  listDocuments: (id: number) => api.get(`/expedientes/${id}/documentos`)
}

// Audiencias
export const audApi = {
  list: (params?: { expediente_id?: number; status?: string }) =>
    api.get('/audiencias', { params }),
  
  get: (id: number) => api.get(`/audiencias/${id}`),
  
  create: (data: any) => api.post('/audiencias', data),
  
  update: (id: number, data: any) => api.put(`/audiencias/${id}`, data),
  
  delete: (id: number) => api.delete(`/audiencias/${id}`),
  
  getProximas: (dias?: number) => api.get('/audiencias/proximas', { params: { dias } }),
  
  marcarRealizada: (id: number, notas?: string) =>
    api.post(`/audiencias/${id}/realizar`, { notas })
}

// Metrics
export const metricsApi = {
  getDashboard: () => api.get('/metrics/dashboard'),
  
  getExpedientes: (params?: { tipo?: string; status?: string }) =>
    api.get('/metrics/expedientes', { params }),
  
  getAudiencias: (days?: number) => api.get('/metrics/audiencias', { params: { days } }),
  
  getTerminos: () => api.get('/metrics/terminos')
}

export default api
