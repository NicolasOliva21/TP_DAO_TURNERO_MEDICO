"""
Gestión de la base de datos usando el patrón Singleton.
Proporciona una única instancia de conexión para toda la aplicación.
"""
from pathlib import Path
from typing import Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import config
from src.domain.base import Base


class DatabaseManager:
    """
    Gestor de base de datos con patrón Singleton.
    Garantiza una única instancia de motor de BD y session factory.
    """

    _instance: Optional["DatabaseManager"] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker] = None

    def __new__(cls) -> "DatabaseManager":
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        """Inicializa el motor de BD y la session factory."""
        if self._engine is not None:
            return  # Ya inicializado

        # Crear motor
        self._engine = create_engine(
            config.DATABASE_URL,
            echo=False,
            pool_pre_ping=True,  # Verifica conexión antes de usar
            connect_args={"check_same_thread": False}  # Para SQLite
        )

        # Crear session factory
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

        print(f"[DB] Base de datos inicializada: {config.DATABASE_URL}")

    def create_tables(self) -> None:
        """Crea todas las tablas en la base de datos."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        Base.metadata.create_all(self._engine)
        print("[DB] Tablas creadas exitosamente")

    def drop_tables(self) -> None:
        """Elimina todas las tablas (solo para testing)."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        Base.metadata.drop_all(self._engine)
        print("[DB] Tablas eliminadas")

    def get_session(self) -> Session:
        """
        Crea y retorna una nueva sesión de BD.
        El llamador es responsable de cerrar la sesión.
        """
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        return self._session_factory()

    @property
    def engine(self) -> Engine:
        """Retorna el motor de BD."""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._engine

    def close(self) -> None:
        """Cierra el motor de BD."""
        if self._engine is not None:
            self._engine.dispose()
            print("[DB] Conexión cerrada")


# Instancia global para facilitar el acceso
db_manager = DatabaseManager()
