"""
Entidad EstadoTurno del dominio.
Representa los posibles estados de un turno.
"""
from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .turno import Turno


class EstadoTurno(Base):
    """
    Entidad que representa un estado de turno.
    
    Los códigos de estado son:
    - PEND: Pendiente
    - CONF: Confirmado
    - CANC: Cancelado
    - ASIS: Asistido
    - INAS: Inasistido
    
    Attributes:
        codigo: Código único del estado
        descripcion: Descripción del estado
        turnos: Lista de turnos con este estado
    """
    
    __tablename__ = "estados_turno"
    
    codigo: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(120), nullable=False)
    
    # Relaciones
    turnos: Mapped[List["Turno"]] = relationship(
        "Turno",
        back_populates="estado"
    )
    
    def __repr__(self) -> str:
        return f"<EstadoTurno(codigo='{self.codigo}', descripcion='{self.descripcion}')>"
    
    def __str__(self) -> str:
        return f"{self.codigo} - {self.descripcion}"
    
    @property
    def es_final(self) -> bool:
        """Indica si el estado es final (no se puede cambiar)."""
        return self.codigo in ['ASIS', 'INAS']
    
    @property
    def es_activo(self) -> bool:
        """Indica si el turno está activo (no cancelado ni finalizado sin asistir)."""
        return self.codigo in ['PEND', 'CONF', 'ASIS']
