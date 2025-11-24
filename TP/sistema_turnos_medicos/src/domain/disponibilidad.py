"""
Entidades relacionadas con la disponibilidad de médicos.
"""
from datetime import time, datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Time, SmallInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .medico import Medico


class DisponibilidadMedico(Base):
    """
    Entidad que representa la disponibilidad semanal de un médico.
    
    Attributes:
        id_medico: ID del médico
        dia_semana: Día de la semana (0=Domingo, 6=Sábado)
        hora_desde: Hora de inicio de atención
        hora_hasta: Hora de fin de atención
        duracion_slot: Duración de cada turno en minutos
        medico: Médico asociado
    """
    
    __tablename__ = "disponibilidades_medico"
    
    dia_semana: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    hora_desde: Mapped[time] = mapped_column(Time, nullable=False)
    hora_hasta: Mapped[time] = mapped_column(Time, nullable=False)
    duracion_slot: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=30)
    
    # Foreign Keys
    id_medico: Mapped[int] = mapped_column(ForeignKey("medicos.id"), nullable=False)
    
    # Relaciones
    medico: Mapped["Medico"] = relationship(
        "Medico",
        back_populates="disponibilidades"
    )
    
    def __repr__(self) -> str:
        dias = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
        return (
            f"<DisponibilidadMedico(medico_id={self.id_medico}, "
            f"dia={dias[self.dia_semana]}, {self.hora_desde}-{self.hora_hasta})>"
        )
    
    def __str__(self) -> str:
        dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        return (
            f"{dias[self.dia_semana]} {self.hora_desde.strftime('%H:%M')} - "
            f"{self.hora_hasta.strftime('%H:%M')} (turnos de {self.duracion_slot}min)"
        )
    
    def valida_horario(self) -> bool:
        """Valida que el horario de inicio sea menor al de fin."""
        return self.hora_desde < self.hora_hasta


class BloqueoMedico(Base):
    """
    Entidad que representa un bloqueo en la agenda del médico.
    Usado para vacaciones, capacitaciones, etc.
    
    Attributes:
        id_medico: ID del médico
        inicio: Fecha y hora de inicio del bloqueo
        fin: Fecha y hora de fin del bloqueo
        motivo: Razón del bloqueo
        medico: Médico asociado
    """
    
    __tablename__ = "bloqueos_medico"
    
    inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    motivo: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Foreign Keys
    id_medico: Mapped[int] = mapped_column(ForeignKey("medicos.id"), nullable=False)
    
    # Relaciones
    medico: Mapped["Medico"] = relationship(
        "Medico",
        back_populates="bloqueos"
    )
    
    def __repr__(self) -> str:
        return (
            f"<BloqueoMedico(medico_id={self.id_medico}, "
            f"desde={self.inicio}, hasta={self.fin})>"
        )
    
    def __str__(self) -> str:
        return (
            f"Bloqueo: {self.inicio.strftime('%d/%m/%Y %H:%M')} - "
            f"{self.fin.strftime('%d/%m/%Y %H:%M')} ({self.motivo or 'Sin motivo'})"
        )
    
    def esta_en_periodo(self, fecha: datetime) -> bool:
        """Verifica si una fecha está dentro del período de bloqueo."""
        return self.inicio <= fecha <= self.fin
