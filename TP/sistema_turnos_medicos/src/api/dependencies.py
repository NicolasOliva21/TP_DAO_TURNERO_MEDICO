"""
Dependencias para la API.
Maneja la inyección de dependencias de FastAPI.
"""
from typing import Generator
from sqlalchemy.orm import Session
from src.repositories.database import db_manager
from src.repositories.unit_of_work import UnitOfWork


def get_db() -> Generator[Session, None, None]:
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en FastAPI.
    """
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()


def get_uow() -> Generator[UnitOfWork, None, None]:
    """
    Generador de Unit of Work.
    Se usa como dependencia en FastAPI.
    """
    uow = UnitOfWork()
    uow.__enter__()  # Inicializar repositorios y sesión
    try:
        yield uow
    finally:
        uow.__exit__(None, None, None)  # Cerrar sesión correctamente
