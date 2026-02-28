"""
Kronaghor - AI Endpoints
Endpoints para el Consultor IA Legal.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.db.database import get_session
from backend.core.security import get_current_user
from backend.models.models import User, ChatMessage
from backend.services.ai_provider import ai_service

router = AIProvider = APIRouter(prefix="/ai", tags=["ai"])


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000


class ChatResponse(BaseModel):
    response: str
    model: str
    provider: str
    usage: dict


class ModelInfo(BaseModel):
    provider: str
    models: List[str]


@router.get("/providers")
def get_providers():
    """Listar proveedores de IA disponibles."""
    providers = ai_service.list_providers()
    return [
        {"name": name, "models": models}
        for name, models in providers.items()
        if models
    ]


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Enviar mensaje al consultor IA legal."""
    
    # Agregar system prompt
    system_prompt = ai_service.legal_system_prompt()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.message}
    ]
    
    # Seleccionar proveedor
    provider = request.provider or ai_service.provider_name
    
    # Llamar al servicio
    result = ai_service.chat(
        messages=messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        provider=provider
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=f"Error del proveedor de IA: {result.get('error', 'Unknown error')}"
        )
    
    # Guardar en historial
    user_id = int(current_user["id"])
    usage = result.get("usage") or {}
    user_msg = ChatMessage(
        user_id=user_id,
        role="user",
        content=request.message,
        model=request.model or provider,
        tokens_used=usage.get("prompt_tokens") if isinstance(usage, dict) else None
    )
    session.add(user_msg)
    
    assistant_msg = ChatMessage(
        user_id=user_id,
        role="assistant",
        content=result["content"],
        model=result.get("model", provider),
        tokens_used=usage.get("completion_tokens") if isinstance(usage, dict) else None
    )
    session.add(assistant_msg)
    session.commit()
    
    return ChatResponse(
        response=result["content"],
        model=result.get("model", provider),
        provider=provider,
        usage=usage if isinstance(usage, dict) else {}
    )


@router.get("/chat/history")
def get_chat_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Obtener historial de chat."""
    user_id = int(current_user["id"])
    
    messages = session.exec(
        select(ChatMessage)
        .where(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    ).all()
    
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "model": m.model,
            "created_at": m.created_at.isoformat()
        }
        for m in messages
    ]


@router.delete("/chat/history")
def clear_chat_history(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Limpiar historial de chat."""
    user_id = int(current_user["id"])
    
    session.exec(
        select(ChatMessage).where(ChatMessage.user_id == user_id)
    )
    session.commit()
    
    return {"message": "Historial limpiado"}
