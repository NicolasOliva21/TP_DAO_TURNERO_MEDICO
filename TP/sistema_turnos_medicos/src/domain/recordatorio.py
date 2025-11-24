"""
Entidad Recordatorio del dominio.
Representa recordatorios automáticos de turnos.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .turno import Turno


class Recordatorio(Base):
    """
    Entidad que representa un recordatorio de turno.
    
    Attributes:
        id_turno: ID del turno
        canal: Canal de envío (EMAIL, PUSH, SMS)
        programado_para: Fecha y hora programada para envío
        enviado_en: Fecha y hora de envío real
        estado: Estado del recordatorio (PENDIENTE, ENVIADO, ERROR)
        error_mensaje: Mensaje de error si falló
        turno: Turno asociado
    """
    
    __tablename__ = "recordatorios"
    
    canal: Mapped[str] = mapped_column(String(20), nullable=False, default="EMAIL")
    programado_para: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    enviado_en: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDIENTE")
    error_mensaje: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Foreign Keys
    id_turno: Mapped[int] = mapped_column(ForeignKey("turnos.id"), nullable=False)
    
    # Relaciones
    turno: Mapped["Turno"] = relationship(
        "Turno",
        back_populates="recordatorios"
    )
    
    def __repr__(self) -> str:
        return (
            f"<Recordatorio(id={self.id}, turno_id={self.id_turno}, "
            f"canal='{self.canal}', estado='{self.estado}')>"
        )
    
    def __str__(self) -> str:
        return (
            f"Recordatorio {self.canal} - "
            f"Programado: {self.programado_para.strftime('%d/%m/%Y %H:%M')} - "
            f"Estado: {self.estado}"
        )
    
    @property
    def fue_enviado(self) -> bool:
        """Indica si el recordatorio fue enviado."""
        return self.estado == "ENVIADO"
    
    @property
    def tuvo_error(self) -> bool:
        """Indica si el recordatorio tuvo error."""
        return self.estado == "ERROR"
    
    def marcar_enviado(self) -> None:
        """Marca el recordatorio como enviado."""
        self.estado = "ENVIADO"
        self.enviado_en = datetime.now()
    
    def marcar_error(self, mensaje: str) -> None:
        """Marca el recordatorio con error."""
        self.estado = "ERROR"
        self.error_mensaje = mensaje
