"""
Kronaghor - Auth Endpoints
Endpoints de autenticación.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from backend.db.database import get_session
from backend.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from backend.models.models import User

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: str = None


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Registrar nuevo usuario."""
    email = user_data.email
    username = user_data.username
    password = user_data.password
    full_name = user_data.full_name
    
    # Verificar si existe
    existing = session.exec(
        select(User).where((User.email == email) | (User.username == username))
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya registrado"
        )
    
    # Crear usuario
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "message": "Usuario registrado exitosamente"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Iniciar sesión."""
    # Buscar usuario
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
    }


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Obtener usuario actual."""
    return current_user
