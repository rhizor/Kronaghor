# Kronaghor 🏛️

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/FastAPI-0.109+-green.svg">
  <img src="https://img.shields.io/badge/TypeScript-5.0+-blue.svg">
  <img src="https://img.shields.io/badge/React-18+-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
</p>

> Asistente Jurídico Colombiano - Optimiza las tareas diarias del ecosistema judicial.

## 📖 Descripción

**Kronaghor** es una plataforma web diseñada para optimizar las tareas diarias en juzgados colombianos. Integra inteligencia artificial para consultas legales, gestión de expedientes, audiencias y métricas de productividad.

## ⚡ Características

- 🤖 **Consultor IA Legal** - Asistencia legal con múltiples proveedores (OpenAI, Grok, Ollama)
- 📁 **Gestor de Expedientes** - CRUD completo de procesos judiciales
- 📅 **Agenda de Audiencias** - Programación y seguimiento de audiencias
- 📊 **Dashboard de Métricas** - Estadísticas de productividad en tiempo real
- 🔐 **Autenticación JWT** - Seguridad con tokens de acceso
- 🗄️ **Base de Datos** - SQLite (desarrollo) / PostgreSQL (producción)

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      KRONAGHOR ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│  │   Frontend  │◄──│    API      │◄──│  Database   │      │
│  │   (React)   │   │  (FastAPI)  │   │  (SQLite)   │      │
│  └─────────────┘   └──────┬──────┘   └─────────────┘      │
│                           │                                 │
│         ┌────────────────┼────────────────┐                │
│         │                │                │                │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐       │
│  │  AI Providers│ │   Services   │ │   Models    │       │
│  │ OpenAI/Grok │ │ Legal/Juris  │ │  SQLModel   │       │
│  │   Ollama    │ │              │ │             │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Instalación

### Requisitos

- Python 3.10+
- Node.js 18+

### Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/rhizor/kronaghor.git
cd kronaghor

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# Copiar configuración
cp .env.example .env
# Editar .env con tus API keys

# Iniciar backend
cd ..
PYTHONPATH=. python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend (otra terminal)
cd frontend
npm install
npm run dev
```

## ⚙️ Configuración

### Variables de Entorno (Backend)

```env
# API
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=tu-secret-key-aqui-change-in-production

# Database (opcional, usa SQLite por defecto)
DATABASE_URL=sqlite:///./kronaghor.db

# AI Providers (configurar al menos uno)
OPENAI_API_KEY=sk-...
GROK_API_KEY=...
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_AI_PROVIDER=ollama

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### AI Providers Soportados

| Proveedor | Modelos | Configuración |
|-----------|---------|---------------|
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-4-turbo | `OPENAI_API_KEY` |
| **Grok** | grok-2-1212, grok-2, grok-beta | `GROK_API_KEY` |
| **Ollama** | Modelos locales | `OLLAMA_BASE_URL` |

## 📡 API Endpoints

### Autenticación
```
POST /api/auth/register  # Registrar usuario
POST /api/auth/login     # Iniciar sesión (OAuth2 form)
GET  /api/auth/me        # Usuario actual
```

### Consultor IA
```
POST /api/ai/chat              # Chat legal
GET  /api/ai/providers         # Listar proveedores
GET  /api/ai/chat/history      # Historial de chats
DELETE /api/ai/chat/history    # Limpiar historial
```

### Expedientes
```
GET    /api/expedientes              # Listar (con filtros)
POST   /api/expedientes              # Crear expediente
GET    /api/expedientes/{id}         # Ver expediente
PUT    /api/expedientes/{id}         # Actualizar
DELETE /api/expedientes/{id}         # Eliminar
POST   /api/expedientes/{id}/documentos  # Subir documento
```

### Audiencias
```
GET    /api/audiencias              # Listar audiencias
POST   /api/audiencias             # Crear audiencia
GET    /api/audiencias/{id}         # Ver audiencia
PUT    /api/audiencias/{id}         # Actualizar
DELETE /api/audiencias/{id}         # Eliminar
GET    /api/audiencias/proximas    # Audiencias próximas
POST   /api/audiencias/{id}/realizar  # Marcar como realizada
```

### Métricas
```
GET /api/metrics/dashboard    # Dashboard general
GET /api/metrics/expedientes  # Métricas de expedientes
GET /api/metrics/audiencias   # Métricas de audiencias
GET /api/metrics/terminos     # Métricas de términos
```

## 🧪 Probando la API

```bash
# Iniciar servidor
PYTHONPATH=. python3 -m uvicorn backend.main:app --port 8001

# 1. Registrar usuario
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"admin","password":"admin123"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r .access_token)

# 3. Crear expediente
curl -X POST http://localhost:8001/api/expedientes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"numero":"2026-001","tipo":"civil","demandante":"Juan","demandado":"Maria"}'

# 4. Chat con IA
curl -X POST http://localhost:8001/api/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"¿Cuál es el término para responder una demanda?"}'
```

## 📁 Estructura del Proyecto

```
kronaghor/
├── backend/
│   ├── api/
│   │   └── endpoints/    # auth, ai, expedientes, audiencias, metrics
│   ├── core/
│   │   ├── config.py     # Configuración
│   │   ├── security.py   # JWT, passwords
│   │   └── logging.py    # Logging
│   ├── models/
│   │   └── models.py     # SQLModel schemas
│   ├── services/
│   │   └── ai_provider.py # OpenAI/Grok/Ollama
│   ├── db/
│   │   └── database.py   # SQLite connection
│   ├── main.py           # App FastAPI
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Sidebar
│   │   ├── pages/        # Login, Dashboard, ConsultorIA, Expedientes, Audiencias
│   │   ├── hooks/        # Zustand stores
│   │   ├── services/     # API client
│   │   └── types/        # TypeScript interfaces
│   ├── package.json
│   └── vite.config.ts
├── docs/                 # Documentación adicional
└── README.md
```

## 📊 Estado del Proyecto

### ✅ Implementado

- [x] Autenticación JWT con registro/login
- [x] CRUD de Expedientes
- [x] CRUD de Audiencias
- [x] Chat con IA (OpenAI, Grok, Ollama)
- [x] Dashboard con métricas
- [x] Historial de chat
- [x] Frontend React completo

### 🔜 Pendiente

- [ ] Integración con Google Drive / OneDrive
- [ ] Notificaciones de términos por vencer
- [ ] Explorador de jurisprudencia (con APIs externas)
- [ ] Tests unitarios
- [ ] Docker Compose

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📜 Licencia

MIT License

---

<p align="center">
  <i>"Justicia delayed is justice denied"</i>
</p>
