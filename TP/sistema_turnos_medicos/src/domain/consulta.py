"""
Entidad Consulta del dominio.
Representa la historia clínica de un turno atendido.
"""
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .turno import Turno
    from .receta import Receta


class Consulta(Base):
    """
    Entidad que representa una consulta médica (historia clínica).
    
    Attributes:
        id_turno: ID del turno atendido (único)
        motivo: Motivo de la consulta
        observaciones: Observaciones del médico
        diagnostico: Diagnóstico médico
        indicaciones: Indicaciones al paciente
        fecha_atencion: Fecha y hora de atención
        turno: Turno asociado
        recetas: Lista de recetas emitidas
    """
    
    __tablename__ = "consultas"
    
    motivo: Mapped[str] = mapped_column(Text, nullable=True)
    observaciones: Mapped[str] = mapped_column(Text, nullable=True)
    diagnostico: Mapped[str] = mapped_column(Text, nullable=True)
    indicaciones: Mapped[str] = mapped_column(Text, nullable=True)
    fecha_atencion: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    # Foreign Keys
    id_turno: Mapped[int] = mapped_column(ForeignKey("turnos.id"), unique=True, nullable=False)
    
    # Relaciones
    turno: Mapped["Turno"] = relationship(
        "Turno",
        back_populates="consulta"
    )
    recetas: Mapped[List["Receta"]] = relationship(
        "Receta",
        back_populates="consulta",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Consulta(id={self.id}, turno_id={self.id_turno}, fecha={self.fecha_atencion})>"
    
    def __str__(self) -> str:
        return (
            f"Consulta del {self.fecha_atencion.strftime('%d/%m/%Y %H:%M')} - "
            f"Diagnóstico: {self.diagnostico[:50] if self.diagnostico else 'N/A'}..."
        )
    
    @property
    def tiene_recetas(self) -> bool:
        """Indica si la consulta tiene recetas asociadas."""
        return len(self.recetas) > 0
