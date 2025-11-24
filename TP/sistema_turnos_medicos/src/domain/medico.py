"""
Entidad Médico del dominio.
Representa a los profesionales médicos.
"""
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseEntity

if TYPE_CHECKING:
    from .especialidad import Especialidad
    from .turno import Turno
    from .disponibilidad import DisponibilidadMedico, BloqueoMedico


# Tabla de asociación para la relación many-to-many
medico_especialidad = Table(
    'medico_especialidad',
    Base.metadata,
    Column('id_medico', ForeignKey('medicos.id'), primary_key=True),
    Column('id_especialidad', ForeignKey('especialidades.id'), primary_key=True)
)


class Medico(Base):
    """
    Entidad que representa un médico.
    
    Attributes:
        matricula: Matrícula profesional (única)
        nombre: Nombre del médico
        apellido: Apellido del médico
        dni: Documento Nacional de Identidad
        genero: Género del médico
        email: Correo electrónico
        telefono: Número de teléfono
        direccion: Dirección física
        especialidades: Lista de especialidades del médico
        turnos: Lista de turnos del médico
        disponibilidades: Horarios de atención
        bloqueos: Períodos no disponibles
    """
    
    __tablename__ = "medicos"
    
    matricula: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)
    dni: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    genero: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    telefono: Mapped[str] = mapped_column(String(30), nullable=False)
    direccion: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Relaciones
    especialidades: Mapped[List["Especialidad"]] = relationship(
        "Especialidad",
        secondary="medico_especialidad",
        back_populates="medicos"
    )
    turnos: Mapped[List["Turno"]] = relationship(
        "Turno",
        back_populates="medico"
    )
    disponibilidades: Mapped[List["DisponibilidadMedico"]] = relationship(
        "DisponibilidadMedico",
        back_populates="medico",
        cascade="all, delete-orphan"
    )
    bloqueos: Mapped[List["BloqueoMedico"]] = relationship(
        "BloqueoMedico",
        back_populates="medico",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Medico(id={self.id}, nombre='{self.nombre_completo}', matricula='{self.matricula}')>"
    
    def __str__(self) -> str:
        especialidades_str = ", ".join(e.nombre for e in self.especialidades[:2])
        if len(self.especialidades) > 2:
            especialidades_str += f" (+{len(self.especialidades) - 2} más)"
        return f"Dr/a. {self.nombre_completo} - Mat. {self.matricula} ({especialidades_str})"
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del médico."""
        return f"{self.apellido}, {self.nombre}"
    
    @property
    def cantidad_turnos(self) -> int:
        """Retorna la cantidad de turnos activos del médico."""
        return len([t for t in self.turnos if t.activo])
    
    def tiene_turnos_pendientes(self) -> bool:
        """Verifica si el médico tiene turnos pendientes o confirmados."""
        from datetime import datetime
        ahora = datetime.now()
        return any(
            t.fecha_hora > ahora and t.activo and t.estado.codigo in ['PEND', 'CONF']
            for t in self.turnos
        )
    
    def tiene_especialidad(self, especialidad_id: int) -> bool:
        """Verifica si el médico tiene una especialidad específica."""
        return any(e.id == especialidad_id for e in self.especialidades)
