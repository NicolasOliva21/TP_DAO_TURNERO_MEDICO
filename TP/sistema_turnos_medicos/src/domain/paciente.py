"""
Entidad Paciente del dominio.
Representa a los pacientes del sistema médico.
"""
from datetime import date
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .turno import Turno


class Paciente(Base):
    """
    Entidad que representa un paciente.
    
    Attributes:
        dni: Documento Nacional de Identidad (único)
        nombre: Nombre del paciente
        apellido: Apellido del paciente
        fecha_nacimiento: Fecha de nacimiento
        genero: Género del paciente
        email: Correo electrónico (único)
        telefono: Número de teléfono
        direccion: Dirección física
        obra_social: Nombre de la obra social
        numero_afiliado: Número de afiliado a la obra social
        turnos: Lista de turnos del paciente
    """
    
    __tablename__ = "pacientes"
    
    dni: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    genero: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    telefono: Mapped[str] = mapped_column(String(30), nullable=False)
    direccion: Mapped[str] = mapped_column(String(200), nullable=False)
    obra_social: Mapped[str] = mapped_column(String(120), nullable=True)
    numero_afiliado: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Relaciones
    turnos: Mapped[List["Turno"]] = relationship(
        "Turno",
        back_populates="paciente",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Paciente(id={self.id}, nombre='{self.nombre_completo}', dni='{self.dni}')>"
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} - DNI: {self.dni}"
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del paciente."""
        return f"{self.apellido}, {self.nombre}"
    
    @property
    def edad(self) -> int:
        """Calcula la edad del paciente."""
        from datetime import date
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    @property
    def cantidad_turnos(self) -> int:
        """Retorna la cantidad de turnos activos del paciente."""
        return len([t for t in self.turnos if t.activo])
    
    def tiene_turnos_futuros(self) -> bool:
        """Verifica si el paciente tiene turnos futuros."""
        from datetime import datetime
        ahora = datetime.now()
        return any(
            t.fecha_hora > ahora and t.activo and t.estado.codigo not in ['CANC', 'INAS']
            for t in self.turnos
        )
