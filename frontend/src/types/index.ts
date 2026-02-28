// Tipos de la aplicación

// User
export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role: string
}

// Auth
export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// Expediente
export interface Expediente {
  id: number
  numero: string
  tipo: string
  status: string
  demandante?: string
  demandado?: string
  objeto?: string
  valor?: number
  fecha_inicio: string
  notas?: string
  tags?: string
  created_at: string
}

export interface ExpedienteCreate {
  numero: string
  tipo?: string
  demandante?: string
  demandado?: string
  objeto?: string
  valor?: number
  notas?: string
  tags?: string
}

// Audiencia
export interface Audiencia {
  id: number
  expediente_id: number
  tipo: string
  fecha: string
  duracion_minutos: number
  lugar?: string
  notas?: string
  status: string
  created_at: string
}

export interface AudienciaCreate {
  expediente_id: number
  tipo: string
  fecha: string
  duracion_minutos?: number
  lugar?: string
  notas?: string
}

// AI Chat
export interface ChatMessage {
  id?: number
  role: 'user' | 'assistant'
  content: string
  model?: string
  created_at?: string
}

export interface ChatRequest {
  message: string
  provider?: string
  model?: string
  temperature?: number
  max_tokens?: number
}

export interface AIProvider {
  name: string
  models: string[]
}

// Metrics
export interface DashboardMetrics {
  total_expedientes: number
  por_estado: Record<string, number>
  por_tipo: Record<string, number>
  audiencias_proximas: number
  terminos_por_vencer: number
  nuevos_30_dias: number
}
