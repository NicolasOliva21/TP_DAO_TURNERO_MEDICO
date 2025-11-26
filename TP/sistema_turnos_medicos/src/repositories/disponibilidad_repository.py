"""Repositorios para Disponibilidad y Bloqueos de Médicos."""
from datetime import date, datetime, time
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.domain.disponibilidad import BloqueoMedico, DisponibilidadMedico
from src.repositories.base_repository import BaseRepository


class DisponibilidadMedicoRepository(BaseRepository[DisponibilidadMedico]):
    """Repositorio para disponibilidades semanales de médicos."""

    def __init__(self, session: Session):
        super().__init__(session, DisponibilidadMedico)

    def get_por_medico(self, medico_id: int) -> List[DisponibilidadMedico]:
        """Obtiene todas las disponibilidades de un médico."""
        stmt = select(DisponibilidadMedico).where(
            DisponibilidadMedico.id_medico == medico_id,
            DisponibilidadMedico.activo == True  # noqa: E712
        ).order_by(DisponibilidadMedico.dia_semana, DisponibilidadMedico.hora_desde)
        
        return list(self.session.scalars(stmt).all())

    def get_por_medico_y_dia(self, medico_id: int, dia_semana: int) -> List[DisponibilidadMedico]:
        """
        Obtiene disponibilidades de un médico para un día específico.
        
        Args:
            medico_id: ID del médico
            dia_semana: Día de la semana (0=Lunes, 6=Domingo)
        """
        stmt = select(DisponibilidadMedico).where(
            DisponibilidadMedico.id_medico == medico_id,
            DisponibilidadMedico.dia_semana == dia_semana,
            DisponibilidadMedico.activo == True  # noqa: E712
        ).order_by(DisponibilidadMedico.hora_desde)
        
        return list(self.session.scalars(stmt).all())

    def verificar_solapamiento(
        self,
        medico_id: int,
        dia_semana: int,
        hora_desde: time,
        hora_hasta: time,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si hay solapamiento de horarios para un médico en un día.
        
        Args:
            medico_id: ID del médico
            dia_semana: Día de la semana
            hora_desde: Hora de inicio
            hora_hasta: Hora de fin
            exclude_id: ID a excluir (para actualizaciones)
        
        Returns:
            True si hay solapamiento, False en caso contrario
        """
        stmt = select(DisponibilidadMedico).where(
            DisponibilidadMedico.id_medico == medico_id,
            DisponibilidadMedico.dia_semana == dia_semana,
            DisponibilidadMedico.activo == True,  # noqa: E712
            # Lógica de solapamiento
            and_(
                DisponibilidadMedico.hora_desde < hora_hasta,
                DisponibilidadMedico.hora_hasta > hora_desde
            )
        )
        
        if exclude_id is not None:
            stmt = stmt.where(DisponibilidadMedico.id != exclude_id)
        
        return self.session.scalar(stmt) is not None


class BloqueoMedicoRepository(BaseRepository[BloqueoMedico]):
    """Repositorio para bloqueos de médicos (vacaciones, etc.)."""

    def __init__(self, session: Session):
        super().__init__(session, BloqueoMedico)

    def get_por_medico(
        self,
        medico_id: int,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> List[BloqueoMedico]:
        """
        Obtiene bloqueos de un médico en un rango de fechas.
        
        Args:
            medico_id: ID del médico
            fecha_desde: Fecha inicial (opcional)
            fecha_hasta: Fecha final (opcional)
        """
        stmt = select(BloqueoMedico).where(
            BloqueoMedico.id_medico == medico_id,
            BloqueoMedico.activo == True  # noqa: E712
        )
        
        if fecha_desde:
            # Bloqueos que terminan después de fecha_desde
            # Convertir date a datetime para comparar con inicio/fin
            fecha_desde_dt = datetime.combine(fecha_desde, time.min)
            stmt = stmt.where(BloqueoMedico.fin >= fecha_desde_dt)
        
        if fecha_hasta:
            # Bloqueos que empiezan antes de fecha_hasta
            fecha_hasta_dt = datetime.combine(fecha_hasta, time.max)
            stmt = stmt.where(BloqueoMedico.inicio <= fecha_hasta_dt)
        
        stmt = stmt.order_by(BloqueoMedico.inicio)
        return list(self.session.scalars(stmt).all())

    def verificar_bloqueado(
        self,
        medico_id: int,
        fecha_hora_inicio: datetime,
        fecha_hora_fin: datetime
    ) -> bool:
        """
        Verifica si el médico está bloqueado en el horario dado.
        
        Args:
            medico_id: ID del médico
            fecha_hora_inicio: Inicio del turno
            fecha_hora_fin: Fin del turno
        
        Returns:
            True si está bloqueado, False en caso contrario
        """
        stmt = select(BloqueoMedico).where(
            BloqueoMedico.id_medico == medico_id,
            BloqueoMedico.activo == True,  # noqa: E712
            # Solapamiento de fechas y horas
            and_(
                BloqueoMedico.inicio < fecha_hora_fin,
                BloqueoMedico.fin > fecha_hora_inicio
            )
        )
        
        resultado = self.session.scalar(stmt)
        return resultado is not None

    def verificar_solapamiento(
        self,
        medico_id: int,
        inicio: datetime,
        fin: datetime,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si hay solapamiento con otros bloqueos del médico.
        
        Args:
            medico_id: ID del médico
            inicio: Fecha y hora de inicio del bloqueo
            fin: Fecha y hora de fin del bloqueo
            exclude_id: ID a excluir (para actualizaciones)
        
        Returns:
            True si hay solapamiento, False en caso contrario
        """
        stmt = select(BloqueoMedico).where(
            BloqueoMedico.id_medico == medico_id,
            BloqueoMedico.activo == True,  # noqa: E712
            and_(
                BloqueoMedico.inicio < fin,
                BloqueoMedico.fin > inicio
            )
        )
        
        if exclude_id is not None:
            stmt = stmt.where(BloqueoMedico.id != exclude_id)
        
        resultado = self.session.scalar(stmt)
        return resultado is not None
