"""
Kronaghor - Logging Module
Configuración de logging para la aplicación.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from backend.core.config import get_settings

settings = get_settings()


def setup_logging(name: str = "kronaghor", log_file: Optional[str] = None) -> logging.Logger:
    """
    Configurar logging para la aplicación.
    
    Args:
        name: Nombre del logger
        log_file: Path opcional para archivo de log
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Default logger
logger = setup_logging()
