"""
Kronaghor - Database Models
Modelos de base de datos usando SQLModel.
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class UserRole(str, Enum):
    """Roles de usuario."""
    ADMIN = "admin"
    JUEZ = "juez"
    SECRETARIO = "secretario"
    ABOGADO = "abogado"
    USER = "user"


class User(SQLModel, table=True):
    """Modelo de usuario."""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: str = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    #expedientes: List["Expediente"] = Relationship(back_populates="user")
    #audiencias: List["Audiencia"] = Relationship(back_populates="user")


class ExpedienteStatus(str, Enum):
    """Estados de expediente."""
    ACTIVO = "activo"
    CERRADO = "cerrado"
    ARCHIVADO = "archivado"
    SUSPENDIDO = "suspendido"


class TipoProceso(str, Enum):
    """Tipos de proceso judicial."""
    CIVIL = "civil"
    PENAL = "penal"
    LABORAL = "laboral"
    CONTENCIOSO = "contencioso"
    ADMINISTRATIVO = "administrativo"
    FAMILIA = "familia"
    OTRO = "otro"


class Expediente(SQLModel, table=True):
    """Modelo de expediente."""
    __tablename__ = "expedientes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    numero: str = Field(unique=True, index=True)
    tipo: str = Field(default=TipoProceso.OTRO)
    status: str = Field(default=ExpedienteStatus.ACTIVO)
    
    # Datos del proceso
    demandante: Optional[str] = None
    demandado: Optional[str] = None
    objeto: Optional[str] = None
    valor: Optional[float] = None
    
    # Fechas
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    fecha_ultima_actualizacion: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None
    
    # Usuario
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Descripción
    notas: Optional[str] = None
    
    # Metadatos
    tags: Optional[str] = None  # JSON string
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Documento(SQLModel, table=True):
    """Modelo de documento."""
    __tablename__ = "documentos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    expediente_id: int = Field(foreign_key="expedientes.id")
    
    nombre: str
    tipo: str  # pdf, docx, etc.
    tamaño: int  # bytes
    
    # Storage
    storage_type: str = Field(default="local")  # local, gdrive, onedrive
    storage_path: Optional[str] = None
    cloud_id: Optional[str] = None  # ID en la nube
    
    # Metadatos
    uploaded_at: datetime = Field(default_factory=datetime.now)
    uploaded_by: Optional[int] = Field(default=None, foreign_key="users.id")


class Audiencia(SQLModel, table=True):
    """Modelo de audiencia."""
    __tablename__ = "audiencias"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    expediente_id: int = Field(foreign_key="expedientes.id")
    
    # Datos de audiencia
    tipo: str  # verbal, escrita, juicio, etc.
    fecha: datetime
    duracion_minutos: int = Field(default=60)
    
    # Estado
    status: str = Field(default="programada")  # programada, realizada, cancelada, reprogramada
    
    # Notas
    lugar: Optional[str] = None
    notas: Optional[str] = None
    
    # Usuario
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Fechas
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ChatMessage(SQLModel, table=True):
    """Modelo de mensaje de chat IA."""
    __tablename__ = "chat_messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    
    # Contenido
    role: str  # user, assistant
    content: str
    model: str  # gpt-4o, grok-2, etc.
    
    # Metadatos
    tokens_used: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Termino(SQLModel, table=True):
    """Modelo de término procesal."""
    __tablename__ = "terminos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    expediente_id: int = Field(foreign_key="expedientes.id")
    
    # Datos del término
    nombre: str  # "Término para responder demanda"
    descripcion: Optional[str] = None
    
    # Fechas
    fecha_inicio: datetime
    fecha_vencimiento: datetime
    
    # Estado
    status: str = Field(default="activo")  # activo, vencido, suspendido
    
    # Notificaciones
    dias_antelacion: int = Field(default=5)  # Días antes de vencer para notificar
    
    # Usuario
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    created_at: datetime = Field(default_factory=datetime.now)


class CloudConfig(SQLModel, table=True):
    """Modelo de configuración de almacenamiento cloud."""
    __tablename__ = "cloud_configs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    
    # Provider
    provider: str  # google, microsoft, local
    
    # Configuración (encrypted)
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    # Estado
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
