"""
Entidad Turno del dominio.
Representa una reserva de turno médico.
"""
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, SmallInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .paciente import Paciente
    from .medico import Medico
    from .especialidad import Especialidad
    from .estado_turno import EstadoTurno
    from .consulta import Consulta
    from .recordatorio import Recordatorio


class Turno(Base):
    """
    Entidad que representa un turno médico.
    
    Attributes:
        id_paciente: ID del paciente
        id_medico: ID del médico
        id_especialidad: ID de la especialidad
        fecha_hora: Fecha y hora del turno
        duracion_minutos: Duración en minutos
        id_estado: ID del estado del turno
        lugar: Lugar de atención (consultorio/sala)
        observaciones: Notas adicionales
        paciente: Paciente asociado
        medico: Médico asociado
        especialidad: Especialidad del turno
        estado: Estado actual del turno
        consulta: Consulta médica (si fue atendido)
        recordatorios: Lista de recordatorios
    """
    
    __tablename__ = "turnos"
    
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    duracion_minutos: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=30)
    lugar: Mapped[str] = mapped_column(String(120), nullable=True)
    observaciones: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Foreign Keys
    id_paciente: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False)
    id_medico: Mapped[int] = mapped_column(ForeignKey("medicos.id"), nullable=False)
    id_especialidad: Mapped[int] = mapped_column(ForeignKey("especialidades.id"), nullable=False)
    id_estado: Mapped[int] = mapped_column(ForeignKey("estados_turno.id"), nullable=False)
    
    # Relaciones
    paciente: Mapped["Paciente"] = relationship(
        "Paciente",
        back_populates="turnos"
    )
    medico: Mapped["Medico"] = relationship(
        "Medico",
        back_populates="turnos"
    )
    especialidad: Mapped["Especialidad"] = relationship(
        "Especialidad",
        back_populates="turnos"
    )
    estado: Mapped["EstadoTurno"] = relationship(
        "EstadoTurno",
        back_populates="turnos"
    )
    consulta: Mapped[Optional["Consulta"]] = relationship(
        "Consulta",
        back_populates="turno",
        uselist=False,
        cascade="all, delete-orphan"
    )
    recordatorios: Mapped[list["Recordatorio"]] = relationship(
        "Recordatorio",
        back_populates="turno",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return (
            f"<Turno(id={self.id}, paciente_id={self.id_paciente}, "
            f"medico_id={self.id_medico}, fecha={self.fecha_hora})>"
        )
    
    def __str__(self) -> str:
        return (
            f"Turno #{self.id} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')} - "
            f"Dr/a. {self.medico.apellido if self.medico else 'N/A'} - "
            f"{self.estado.descripcion if self.estado else 'N/A'}"
        )
    
    @property
    def fecha_hora_fin(self) -> datetime:
        """Calcula la fecha y hora de fin del turno."""
        return self.fecha_hora + timedelta(minutes=self.duracion_minutos)
    
    @property
    def es_futuro(self) -> bool:
        """Indica si el turno es futuro."""
        return self.fecha_hora > datetime.now()
    
    @property
    def es_pasado(self) -> bool:
        """Indica si el turno es pasado."""
        return self.fecha_hora < datetime.now()
    
    @property
    def puede_modificarse(self) -> bool:
        """Indica si el turno puede modificarse."""
        return self.estado.codigo in ['PEND', 'CONF'] and self.es_futuro
    
    @property
    def puede_cancelarse(self) -> bool:
        """Indica si el turno puede cancelarse."""
        return self.puede_modificarse
    
    def solapa_con(self, otro_turno: "Turno") -> bool:
        """
        Verifica si este turno se solapa con otro turno.
        
        Args:
            otro_turno: Otro turno a comparar
            
        Returns:
            True si hay solapamiento, False en caso contrario
        """
        inicio1 = self.fecha_hora
        fin1 = self.fecha_hora_fin
        inicio2 = otro_turno.fecha_hora
        fin2 = otro_turno.fecha_hora_fin
        
        return not (fin1 <= inicio2 or fin2 <= inicio1)
