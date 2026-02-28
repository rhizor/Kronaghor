"""
Kronaghor - Database Connection
Maneja la conexión a la base de datos.
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from backend.core.config import get_settings

settings = get_settings()


def get_database_url() -> str:
    """Obtener URL de base de datos."""
    return settings.DATABASE_URL


def create_db_engine():
    """Crear engine de base de datos."""
    engine = create_engine(
        get_database_url(),
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False} if "sqlite" in get_database_url() else {}
    )
    return engine


def create_db_and_tables():
    """Crear tablas en la base de datos."""
    engine = create_db_engine()
    SQLModel.metadata.create_all(engine)


# Engine singleton
engine = create_db_engine()


def get_session() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de base de datos.
    
    Usage:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def get_session_sync() -> Session:
    """Obtener sesión síncrona."""
    return Session(engine)
