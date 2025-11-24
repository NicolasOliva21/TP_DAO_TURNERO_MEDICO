"""Repositorio para la entidad Recordatorio."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.domain.recordatorio import Recordatorio
from src.repositories.base_repository import BaseRepository


class RecordatorioRepository(BaseRepository[Recordatorio]):
    """Repositorio para Recordatorios de turnos."""

    def __init__(self, session: Session):
        super().__init__(session, Recordatorio)

    def get_por_turno(self, turno_id: int) -> List[Recordatorio]:
        """
        Obtiene todos los recordatorios de un turno.
        
        Args:
            turno_id: ID del turno
        
        Returns:
            Lista de recordatorios
        """
        stmt = select(Recordatorio).where(
            Recordatorio.id_turno == turno_id,
            Recordatorio.activo == True  # noqa: E712
        ).order_by(Recordatorio.programado_para.desc())
        
        return list(self.session.scalars(stmt).all())

    def get_pendientes_de_envio(
        self,
        hasta: Optional[datetime] = None
    ) -> List[Recordatorio]:
        """
        Obtiene recordatorios pendientes de envío.
        
        Args:
            hasta: Fecha/hora límite para envío (opcional, por defecto ahora)
        
        Returns:
            Lista de recordatorios PENDIENTE que deben enviarse
        """
        if hasta is None:
            hasta = datetime.now()
        
        stmt = select(Recordatorio).options(
            joinedload(Recordatorio.turno).joinedload("paciente"),
            joinedload(Recordatorio.turno).joinedload("medico"),
            joinedload(Recordatorio.turno).joinedload("especialidad")
        ).where(
            Recordatorio.activo == True,  # noqa: E712
            Recordatorio.estado == "PENDIENTE",
            Recordatorio.programado_para <= hasta
        ).order_by(Recordatorio.programado_para)
        
        return list(self.session.scalars(stmt).unique().all())

    def existe_para_turno(self, turno_id: int, canal: str) -> bool:
        """
        Verifica si ya existe un recordatorio para el turno y canal dados.
        
        Args:
            turno_id: ID del turno
            canal: Canal de envío (EMAIL, PUSH, SMS)
        
        Returns:
            True si existe, False en caso contrario
        """
        stmt = select(Recordatorio).where(
            Recordatorio.id_turno == turno_id,
            Recordatorio.canal == canal,
            Recordatorio.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt) is not None

    def get_enviados_hoy(self) -> List[Recordatorio]:
        """Obtiene recordatorios enviados hoy."""
        hoy_inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        hoy_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        stmt = select(Recordatorio).where(
            Recordatorio.activo == True,  # noqa: E712
            Recordatorio.estado == "ENVIADO",
            Recordatorio.enviado_en >= hoy_inicio,
            Recordatorio.enviado_en <= hoy_fin
        ).order_by(Recordatorio.enviado_en.desc())
        
        return list(self.session.scalars(stmt).all())
