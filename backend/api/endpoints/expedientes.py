"""
Kronaghor - Expedientes Endpoints
Endpoints para gestión de expedientes.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.db.database import get_session
from backend.core.security import get_current_user
from backend.models.models import Expediente, Documento, ExpedienteStatus, TipoProceso

router = APIRouter(prefix="/expedientes", tags=["expedientes"])


# Request/Response models
class ExpedienteCreate(BaseModel):
    numero: str
    tipo: str = "otro"
    demandante: Optional[str] = None
    demandado: Optional[str] = None
    objeto: Optional[str] = None
    valor: Optional[float] = None
    notas: Optional[str] = None
    tags: Optional[str] = None


class ExpedienteUpdate(BaseModel):
    tipo: Optional[str] = None
    status: Optional[str] = None
    demandante: Optional[str] = None
    demandado: Optional[str] = None
    objeto: Optional[str] = None
    valor: Optional[float] = None
    notas: Optional[str] = None
    tags: Optional[str] = None


class ExpedienteResponse(BaseModel):
    id: int
    numero: str
    tipo: str
    status: str
    demandante: Optional[str]
    demandado: Optional[str]
    objeto: Optional[str]
    valor: Optional[float]
    fecha_inicio: datetime
    notas: Optional[str]
    tags: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("", response_model=List[ExpedienteResponse])
def list_expedientes(
    status: Optional[str] = None,
    tipo: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Listar expedientes."""
    query = select(Expediente)
    
    if status:
        query = query.where(Expediente.status == status)
    if tipo:
        query = query.where(Expediente.tipo == tipo)
    if search:
        query = query.where(
            (Expediente.numero.contains(search)) |
            (Expediente.demandante.contains(search)) |
            (Expediente.demandado.contains(search))
        )
    
    query = query.order_by(Expediente.created_at.desc()).limit(limit).offset(offset)
    
    return session.exec(query).all()


@router.get("/{expediente_id}", response_model=ExpedienteResponse)
def get_expediente(
    expediente_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Obtener expediente por ID."""
    exp = session.get(Expediente, expediente_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return exp


@router.post("", response_model=ExpedienteResponse)
def create_expediente(
    expediente: ExpedienteCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Crear nuevo expediente."""
    # Verificar si existe
    existing = session.exec(
        select(Expediente).where(Expediente.numero == expediente.numero)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Número de expediente ya existe")
    
    # Crear
    exp = Expediente(
        numero=expediente.numero,
        tipo=expediente.tipo,
        demandante=expediente.demandante,
        demandado=expediente.demandado,
        objeto=expediente.objeto,
        valor=expediente.valor,
        notas=expediente.notas,
        tags=expediente.tags,
        user_id=int(current_user["id"])
    )
    
    session.add(exp)
    session.commit()
    session.refresh(exp)
    
    return exp


@router.put("/{expediente_id}", response_model=ExpedienteResponse)
def update_expediente(
    expediente_id: int,
    expediente: ExpedienteUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Actualizar expediente."""
    exp = session.get(Expediente, expediente_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    
    # Actualizar campos
    update_data = expediente.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exp, field, value)
    
    exp.updated_at = datetime.now()
    
    session.add(exp)
    session.commit()
    session.refresh(exp)
    
    return exp


@router.delete("/{expediente_id}")
def delete_expediente(
    expediente_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Eliminar expediente."""
    exp = session.get(Expediente, expediente_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    
    session.delete(exp)
    session.commit()
    
    return {"message": "Expediente eliminado"}


# Documentos
@router.post("/{expediente_id}/documentos")
async def upload_documento(
    expediente_id: int,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Subir documento a expediente."""
    # Verificar expediente
    exp = session.get(Expediente, expediente_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    
    # Guardar archivo
    import os
    from pathlib import Path
    
    upload_dir = Path("uploads") / str(expediente_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / file.filename
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Crear registro
    doc = Documento(
        expediente_id=expediente_id,
        nombre=file.filename,
        tipo=file.content_type or "application/octet-stream",
        tamaño=len(content),
        storage_type="local",
        storage_path=str(file_path),
        uploaded_by=int(current_user["id"])
    )
    
    session.add(doc)
    session.commit()
    
    return {"id": doc.id, "filename": file.filename, "size": len(content)}


@router.get("/{expediente_id}/documentos")
def list_documentos(
    expediente_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Listar documentos de expediente."""
    docs = session.exec(
        select(Documento)
        .where(Documento.expediente_id == expediente_id)
        .order_by(Documento.uploaded_at.desc())
    ).all()
    
    return [
        {
            "id": d.id,
            "nombre": d.nombre,
            "tipo": d.tipo,
            "tamaño": d.tamaño,
            "uploaded_at": d.uploaded_at.isoformat()
        }
        for d in docs
    ]
