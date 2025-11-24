"""
Entidad Especialidad del dominio.
Representa las especialidades médicas.
"""
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .medico import Medico
    from .turno import Turno


class Especialidad(Base):
    """
    Entidad que representa una especialidad médica.
    
    Attributes:
        nombre: Nombre de la especialidad (único)
        descripcion: Descripción detallada
        medicos: Lista de médicos con esta especialidad
        turnos: Lista de turnos para esta especialidad
    """
    
    __tablename__ = "especialidades"
    
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relaciones
    medicos: Mapped[List["Medico"]] = relationship(
        "Medico",
        secondary="medico_especialidad",
        back_populates="especialidades"
    )
    turnos: Mapped[List["Turno"]] = relationship(
        "Turno",
        back_populates="especialidad"
    )
    
    def __repr__(self) -> str:
        return f"<Especialidad(id={self.id}, nombre='{self.nombre}')>"
    
    def __str__(self) -> str:
        return self.nombre
    
    @property
    def cantidad_medicos(self) -> int:
        """Retorna la cantidad de médicos activos en la especialidad."""
        return len([m for m in self.medicos if m.activo])
    
    @property
    def cantidad_turnos(self) -> int:
        """Retorna la cantidad de turnos activos de la especialidad."""
        return len([t for t in self.turnos if t.activo])
    
    def tiene_medicos_o_turnos(self) -> bool:
        """Verifica si la especialidad tiene médicos o turnos asociados."""
        return self.cantidad_medicos > 0 or self.cantidad_turnos > 0
