"""
Kronaghor - Main Application
Punto de entrada de la API FastAPI.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import get_settings
from backend.core.logging import logger
from backend.db.database import create_db_and_tables

from backend.api.endpoints import auth, ai, expedientes, audiencias, metrics

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    logger.info("Iniciando Kronaghor...")
    create_db_and_tables()
    logger.info("Base de datos inicializada")
    yield
    logger.info("Apagando Kronaghor...")


# Create FastAPI app
app = FastAPI(
    title="Kronaghor API",
    description="API del Asistente Jurídico Colombiano",
    version="2.0.0",
    docs="/docs",
    redoc="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": "Kronaghor",
        "version": "2.0.0",
        "description": "Asistente Jurídico Colombiano"
    }


@app.get("/health")
def health_check():
    """Health check."""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(expedientes.router, prefix="/api")
app.include_router(audiencias.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
