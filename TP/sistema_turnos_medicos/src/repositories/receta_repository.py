"""Repositorios para Receta e ItemReceta."""
from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.domain.receta import ItemReceta, Receta
from src.repositories.base_repository import BaseRepository


class RecetaRepository(BaseRepository[Receta]):
    """Repositorio para Recetas médicas."""

    def __init__(self, session: Session):
        super().__init__(session, Receta)

    def get_by_id_completa(self, receta_id: int) -> Optional[Receta]:
        """Obtiene receta con todos los items cargados."""
        stmt = select(Receta).options(
            joinedload(Receta.items),
            joinedload(Receta.consulta).joinedload("turno").joinedload("paciente"),
            joinedload(Receta.consulta).joinedload("turno").joinedload("medico")
        ).where(
            Receta.id == receta_id,
            Receta.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def get_por_consulta(self, consulta_id: int) -> List[Receta]:
        """
        Obtiene todas las recetas de una consulta.
        
        Args:
            consulta_id: ID de la consulta
        
        Returns:
            Lista de recetas con sus items
        """
        stmt = select(Receta).options(
            joinedload(Receta.items)
        ).where(
            Receta.id_consulta == consulta_id,
            Receta.activo == True  # noqa: E712
        ).order_by(Receta.fecha_emision.desc())
        
        return list(self.session.scalars(stmt).unique().all())

    def get_por_paciente(
        self,
        paciente_id: int,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        solo_activas: bool = False
    ) -> List[Receta]:
        """
        Obtiene recetas de un paciente.
        
        Args:
            paciente_id: ID del paciente
            fecha_desde: Fecha inicial (opcional)
            fecha_hasta: Fecha final (opcional)
            solo_activas: Si es True, solo recetas ACTIVAS
        
        Returns:
            Lista de recetas con sus items
        """
        stmt = select(Receta).join(
            Receta.consulta
        ).join(
            "turno"
        ).options(
            joinedload(Receta.items),
            joinedload(Receta.consulta).joinedload("turno").joinedload("medico")
        ).where(
            Receta.consulta.has(turno={"id_paciente": paciente_id}),
            Receta.activo == True  # noqa: E712
        )
        
        if fecha_desde:
            stmt = stmt.where(Receta.fecha_emision >= fecha_desde)
        
        if fecha_hasta:
            stmt = stmt.where(Receta.fecha_emision <= fecha_hasta)
        
        if solo_activas:
            stmt = stmt.where(Receta.estado == "ACTIVA")
        
        stmt = stmt.order_by(Receta.fecha_emision.desc())
        return list(self.session.scalars(stmt).unique().all())

    def get_por_medico(
        self,
        medico_id: int,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> List[Receta]:
        """
        Obtiene recetas emitidas por un médico.
        
        Args:
            medico_id: ID del médico
            fecha_desde: Fecha inicial (opcional)
            fecha_hasta: Fecha final (opcional)
        
        Returns:
            Lista de recetas con sus items
        """
        stmt = select(Receta).join(
            Receta.consulta
        ).join(
            "turno"
        ).options(
            joinedload(Receta.items),
            joinedload(Receta.consulta).joinedload("turno").joinedload("paciente")
        ).where(
            Receta.consulta.has(turno={"id_medico": medico_id}),
            Receta.activo == True  # noqa: E712
        )
        
        if fecha_desde:
            stmt = stmt.where(Receta.fecha_emision >= fecha_desde)
        
        if fecha_hasta:
            stmt = stmt.where(Receta.fecha_emision <= fecha_hasta)
        
        stmt = stmt.order_by(Receta.fecha_emision.desc())
        return list(self.session.scalars(stmt).unique().all())


class ItemRecetaRepository(BaseRepository[ItemReceta]):
    """Repositorio para Items de Receta."""

    def __init__(self, session: Session):
        super().__init__(session, ItemReceta)

    def get_por_receta(self, receta_id: int) -> List[ItemReceta]:
        """
        Obtiene todos los items de una receta.
        
        Args:
            receta_id: ID de la receta
        
        Returns:
            Lista de items de la receta
        """
        stmt = select(ItemReceta).where(
            ItemReceta.id_receta == receta_id,
            ItemReceta.activo == True  # noqa: E712
        )
        return list(self.session.scalars(stmt).all())
