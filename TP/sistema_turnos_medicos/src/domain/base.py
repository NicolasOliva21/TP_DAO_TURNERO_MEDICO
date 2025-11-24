"""
Módulo base para las entidades del dominio.
Define la clase base para todas las entidades.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Clase base para todas las entidades del dominio.
    Combina DeclarativeBase de SQLAlchemy con campos comunes.
    """
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        nullable=False
    )
    fecha_modificacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        default=None,
        onupdate=datetime.now,
        nullable=True
    )
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def soft_delete(self) -> None:
        """Realiza un borrado lógico de la entidad."""
        self.activo = False
        self.fecha_modificacion = datetime.now()
    
    def restore(self) -> None:
        """Restaura una entidad borrada lógicamente."""
        self.activo = True
        self.fecha_modificacion = datetime.now()


# Alias para compatibilidad con código existente
BaseEntity = Base
