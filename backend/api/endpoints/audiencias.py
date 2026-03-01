"""
Kronaghor - Audiencias Endpoints
Endpoints para gestión de audiencias.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from backend.db.database import get_session
from backend.core.security import get_current_user
from backend.models.models import Audiencia, Expediente

router = APIRouter(prefix="/audiencias", tags=["audiencias"])


# Request/Response models
class AudienciaCreate(BaseModel):
    expediente_id: int
    tipo: str
    fecha: datetime
    duracion_minutos: int = 60
    lugar: Optional[str] = None
    notas: Optional[str] = None


class AudienciaUpdate(BaseModel):
    tipo: Optional[str] = None
    fecha: Optional[datetime] = None
    duracion_minutos: Optional[int] = None
    lugar: Optional[str] = None
    notas: Optional[str] = None
    status: Optional[str] = None


class AudienciaResponse(BaseModel):
    id: int
    expediente_id: int
    tipo: str
    fecha: datetime
    duracion_minutos: int
    lugar: Optional[str]
    notas: Optional[str]
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


@router.get("", response_model=List[AudienciaResponse])
def list_audiencias(
    expediente_id: Optional[int] = None,
    status: Optional[str] = None,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Listar audiencias."""
    query = select(Audiencia)
    
    if expediente_id:
        query = query.where(Audiencia.expediente_id == expediente_id)
    if status:
        query = query.where(Audiencia.status == status)
    if desde:
        query = query.where(Audiencia.fecha >= desde)
    if hasta:
        query = query.where(Audiencia.fecha <= hasta)
    
    query = query.order_by(Audiencia.fecha.asc()).limit(limit).offset(offset)
    
    return session.exec(query).all()


@router.get("/proximas")
def get_proximas_audiencias(
    dias: int = 7,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Obtener audiencias próximas."""
    hoy = datetime.now()
    hasta = hoy + timedelta(days=dias)
    
    audiencias = session.exec(
        select(Audiencia)
        .where(Audiencia.fecha >= hoy)
        .where(Audiencia.fecha <= hasta)
        .where(Audiencia.status == "programada")
        .order_by(Audiencia.fecha.asc())
    ).all()
    
    result = []
    for aud in audiencias:
        exp = session.get(Expediente, aud.expediente_id)
        result.append({
            "id": aud.id,
            "expediente_id": aud.expediente_id,
            "expediente_numero": exp.numero if exp else "N/A",
            "tipo": aud.tipo,
            "fecha": aud.fecha.isoformat(),
            "duracion": aud.duracion_minutos,
            "lugar": aud.lugar,
            "status": aud.status
        })
    
    return result


@router.get("/{audiencia_id}", response_model=AudienciaResponse)
def get_audiencia(
    audiencia_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Obtener audiencia por ID."""
    aud = session.get(Audiencia, audiencia_id)
    if not aud:
        raise HTTPException(status_code=404, detail="Audiencia no encontrada")
    return aud


@router.post("", response_model=AudienciaResponse)
def create_audiencia(
    audiencia: AudienciaCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Crear nueva audiencia."""
    # Verificar expediente
    exp = session.get(Expediente, audiencia.expediente_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    
    # Crear audiencia
    aud = Audiencia(
        expediente_id=audiencia.expediente_id,
        tipo=audiencia.tipo,
        fecha=audiencia.fecha,
        duracion_minutos=audiencia.duracion_minutos,
        lugar=audiencia.lugar,
        notas=audiencia.notas,
        user_id=int(current_user["id"])
    )
    
    session.add(aud)
    session.commit()
    session.refresh(aud)
    
    return aud


@router.put("/{audiencia_id}", response_model=AudienciaResponse)
def update_audiencia(
    audiencia_id: int,
    audiencia: AudienciaUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Actualizar audiencia."""
    aud = session.get(Audiencia, audiencia_id)
    if not aud:
        raise HTTPException(status_code=404, detail="Audiencia no encontrada")
    
    # Actualizar campos
    update_data = audiencia.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(aud, field, value)
    
    aud.updated_at = datetime.now()
    
    session.add(aud)
    session.commit()
    session.refresh(aud)
    
    return aud


@router.delete("/{audiencia_id}")
def delete_audiencia(
    audiencia_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Eliminar audiencia."""
    aud = session.get(Audiencia, audiencia_id)
    if not aud:
        raise HTTPException(status_code=404, detail="Audiencia no encontrada")
    
    session.delete(aud)
    session.commit()
    
    return {"message": "Audiencia eliminada"}


@router.post("/{audiencia_id}/realizar")
def marcar_realizada(
    audiencia_id: int,
    notas: str = None,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Marcar audiencia como realizada."""
    aud = session.get(Audiencia, audiencia_id)
    if not aud:
        raise HTTPException(status_code=404, detail="Audiencia no encontrada")
    
    aud.status = "realizada"
    if notas:
        aud.notas = (aud.notas or "") + f"\n\n--- Notas de realización ---\n{notas}"
    
    session.add(aud)
    session.commit()
    
    return {"message": "Audiencia marcada como realizada"}
