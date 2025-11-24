"""
Entidades relacionadas con las recetas médicas.
"""
from datetime import date
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .consulta import Consulta


class Receta(Base):
    """
    Entidad que representa una receta médica electrónica.
    
    Attributes:
        id_consulta: ID de la consulta
        fecha_emision: Fecha de emisión
        estado: Estado de la receta (ACTIVA, ANULADA, EXPIRADA)
        firma_hash: Hash de firma digital del médico
        consulta: Consulta asociada
        items: Lista de medicamentos recetados
    """
    
    __tablename__ = "recetas"
    
    fecha_emision: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVA")
    firma_hash: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Foreign Keys
    id_consulta: Mapped[int] = mapped_column(ForeignKey("consultas.id"), nullable=False)
    
    # Relaciones
    consulta: Mapped["Consulta"] = relationship(
        "Consulta",
        back_populates="recetas"
    )
    items: Mapped[List["ItemReceta"]] = relationship(
        "ItemReceta",
        back_populates="receta",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Receta(id={self.id}, consulta_id={self.id_consulta}, estado='{self.estado}')>"
    
    def __str__(self) -> str:
        return (
            f"Receta #{self.id} - {self.fecha_emision.strftime('%d/%m/%Y')} - "
            f"{self.estado} ({len(self.items)} medicamento(s))"
        )
    
    @property
    def es_valida(self) -> bool:
        """Indica si la receta está activa."""
        return self.estado == "ACTIVA"
    
    def anular(self) -> None:
        """Anula la receta."""
        self.estado = "ANULADA"
    
    def marcar_expirada(self) -> None:
        """Marca la receta como expirada."""
        self.estado = "EXPIRADA"


class ItemReceta(Base):
    """
    Entidad que representa un medicamento en una receta.
    
    Attributes:
        id_receta: ID de la receta
        medicamento: Nombre del medicamento
        dosis: Dosis prescrita
        frecuencia: Frecuencia de administración
        duracion: Duración del tratamiento
        indicaciones: Indicaciones especiales
        receta: Receta asociada
    """
    
    __tablename__ = "items_receta"
    
    medicamento: Mapped[str] = mapped_column(String(200), nullable=False)
    dosis: Mapped[str] = mapped_column(String(160), nullable=True)
    frecuencia: Mapped[str] = mapped_column(String(160), nullable=True)
    duracion: Mapped[str] = mapped_column(String(160), nullable=True)
    indicaciones: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Foreign Keys
    id_receta: Mapped[int] = mapped_column(ForeignKey("recetas.id"), nullable=False)
    
    # Relaciones
    receta: Mapped["Receta"] = relationship(
        "Receta",
        back_populates="items"
    )
    
    def __repr__(self) -> str:
        return f"<ItemReceta(id={self.id}, medicamento='{self.medicamento}', dosis='{self.dosis}')>"
    
    def __str__(self) -> str:
        return (
            f"{self.medicamento} - {self.dosis or 'N/A'} - "
            f"{self.frecuencia or 'N/A'} durante {self.duracion or 'N/A'}"
        )
