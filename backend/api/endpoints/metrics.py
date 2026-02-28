"""
Kronaghor - Métricas Endpoints
Endpoints para dashboard y métricas.
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from backend.db.database import get_session
from backend.core.security import get_current_user
from backend.models.models import Expediente, Audiencia, Termino

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/dashboard")
def get_dashboard(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Obtener datos del dashboard."""
    hoy = datetime.now()
    hace_30_dias = hoy - timedelta(days=30)
    
    # Total expedientes
    total_expedientes = session.exec(
        select(func.count(Expediente.id))
    ).one()
    
    # Expedientes por estado
    por_estado = {}
    for status in ["activo", "cerrado", "archivado", "suspendido"]:
        count = session.exec(
            select(func.count(Expediente.id)).where(Expediente.status == status)
        ).one()
        por_estado[status] = count
    
    # Expedientes por tipo
    por_tipo = {}
    tipos = session.exec(
        select(Expediente.tipo).distinct()
    ).all()
    for tipo in tipos:
        count = session.exec(
            select(func.count(Expediente.id)).where(Expediente.tipo == tipo)
        ).one()
        por_tipo[tipo] = count
    
    # Audiencias próximas
    audiencias_proximas = session.exec(
        select(func.count(Audiencia.id))
        .where(Audiencia.fecha >= hoy)
        .where(Audiencia.status == "programada")
    ).one()
    
    # Términos por vencer
    terminos_por_vencer = session.exec(
        select(func.count(Termino.id))
        .where(Termino.fecha_vencimiento >= hoy)
        .where(Termino.fecha_vencimiento <= hoy + timedelta(days=7))
        .where(Termino.status == "activo")
    ).one()
    
    # Expedientes últimos 30 días
    nuevos_expedientes = session.exec(
        select(func.count(Expediente.id))
        .where(Expediente.created_at >= hace_30_dias)
    ).one()
    
    return {
        "total_expedientes": total_expedientes,
        "por_estado": por_estado,
        "por_tipo": por_tipo,
        "audiencias_proximas": audiencias_proximas,
        "terminos_por_vencer": terminos_por_vencer,
        "nuevos_30_dias": nuevos_expedientes
    }


@router.get("/expedientes")
def get_metrics_expedientes(
    tipo: Optional[str] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Métricas de expedientes."""
    query = select(
        Expediente.tipo,
        Expediente.status,
        func.count(Expediente.id).label("count")
    ).group_by(Expediente.tipo, Expediente.status)
    
    if tipo:
        query = query.where(Expediente.tipo == tipo)
    if status:
        query = query.where(Expediente.status == status)
    
    results = session.exec(query).all()
    
    return [
        {"tipo": r.tipo, "status": r.status, "count": r.count}
        for r in results
    ]


@router.get("/audiencias")
def get_metrics_audiencias(
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Métricas de audiencias."""
    desde = datetime.now() - timedelta(days=days)
    
    # Totales por status
    por_status = {}
    for status in ["programada", "realizada", "cancelada", "reprogramada"]:
        count = session.exec(
            select(func.count(Audiencia.id))
            .where(Audiencia.status == status)
            .where(Audiencia.fecha >= desde)
        ).one()
        por_status[status] = count
    
    # Total
    total = sum(por_status.values())
    
    return {
        "periodo_dias": days,
        "total": total,
        "por_status": por_status
    }


@router.get("/terminos")
def get_metrics_terminos(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Métricas de términos procesales."""
    hoy = datetime.now()
    
    # Activos
    activos = session.exec(
        select(func.count(Termino.id))
        .where(Termino.status == "activo")
    ).one()
    
    # Por vencer (7 días)
    por_vencer = session.exec(
        select(func.count(Termino.id))
        .where(Termino.fecha_vencimiento >= hoy)
        .where(Termino.fecha_vencimiento <= hoy + timedelta(days=7))
        .where(Termino.status == "activo")
    ).one()
    
    # Vencidos
    vencidos = session.exec(
        select(func.count(Termino.id))
        .where(Termino.fecha_vencimiento < hoy)
        .where(Termino.status == "activo")
    ).one()
    
    return {
        "activos": activos,
        "por_vencer_7_dias": por_vencer,
        "vencidos": vencidos
    }
