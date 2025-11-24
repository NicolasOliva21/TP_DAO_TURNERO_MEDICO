"""Repositorio para la entidad EstadoTurno."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.estado_turno import EstadoTurno
from src.repositories.base_repository import BaseRepository


class EstadoTurnoRepository(BaseRepository[EstadoTurno]):
    """Repositorio específico para Estados de Turno."""

    def __init__(self, session: Session):
        super().__init__(session, EstadoTurno)

    def get_by_codigo(self, codigo: str) -> Optional[EstadoTurno]:
        """
        Busca estado por código (PEND, CONF, CANC, ASIS, INAS).
        
        Args:
            codigo: Código del estado
        
        Returns:
            Estado de turno o None si no existe
        """
        stmt = select(EstadoTurno).where(
            EstadoTurno.codigo == codigo,
            EstadoTurno.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def get_pendiente(self) -> Optional[EstadoTurno]:
        """Obtiene el estado PENDIENTE."""
        return self.get_by_codigo("PEND")

    def get_confirmado(self) -> Optional[EstadoTurno]:
        """Obtiene el estado CONFIRMADO."""
        return self.get_by_codigo("CONF")

    def get_cancelado(self) -> Optional[EstadoTurno]:
        """Obtiene el estado CANCELADO."""
        return self.get_by_codigo("CANC")

    def get_asistido(self) -> Optional[EstadoTurno]:
        """Obtiene el estado ASISTIDO."""
        return self.get_by_codigo("ASIS")

    def get_inasistido(self) -> Optional[EstadoTurno]:
        """Obtiene el estado INASISTIDO."""
        return self.get_by_codigo("INAS")
