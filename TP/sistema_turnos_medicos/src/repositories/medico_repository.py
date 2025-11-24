"""Repositorio para la entidad Médico."""
from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from src.domain.medico import Medico
from src.repositories.base_repository import BaseRepository


class MedicoRepository(BaseRepository[Medico]):
    """Repositorio específico para Médicos."""

    def __init__(self, session: Session):
        super().__init__(session, Medico)

    def get_by_matricula(self, matricula: str) -> Optional[Medico]:
        """Busca médico por matrícula (solo activos)."""
        stmt = select(Medico).where(
            Medico.matricula == matricula,
            Medico.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def get_by_id_con_especialidades(self, medico_id: int) -> Optional[Medico]:
        """Obtiene médico por ID con sus especialidades cargadas."""
        stmt = select(Medico).options(
            joinedload(Medico.especialidades)
        ).where(
            Medico.id == medico_id,
            Medico.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def exists_matricula(self, matricula: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un médico activo con la matrícula dada.
        
        Args:
            matricula: Matrícula a verificar
            exclude_id: ID de médico a excluir (útil para actualizaciones)
        """
        stmt = select(Medico).where(
            Medico.matricula == matricula,
            Medico.activo == True  # noqa: E712
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Medico.id != exclude_id)
        
        return self.session.scalar(stmt) is not None

    def exists_dni(self, dni: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe un médico activo con el DNI dado."""
        stmt = select(Medico).where(
            Medico.dni == dni,
            Medico.activo == True  # noqa: E712
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Medico.id != exclude_id)
        
        return self.session.scalar(stmt) is not None

    def exists_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe un médico activo con el email dado."""
        stmt = select(Medico).where(
            Medico.email == email.lower(),
            Medico.activo == True  # noqa: E712
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Medico.id != exclude_id)
        
        return self.session.scalar(stmt) is not None

    def buscar(self, texto: str) -> List[Medico]:
        """
        Búsqueda por nombre, apellido, matrícula o DNI.
        
        Args:
            texto: Texto a buscar
        
        Returns:
            Lista de médicos que coinciden con la búsqueda
        """
        texto_lower = f"%{texto.lower()}%"
        
        stmt = select(Medico).where(
            Medico.activo == True,  # noqa: E712
            or_(
                Medico.nombre.ilike(texto_lower),
                Medico.apellido.ilike(texto_lower),
                Medico.matricula.like(f"%{texto}%"),
                Medico.dni.like(f"%{texto}%")
            )
        ).options(joinedload(Medico.especialidades))
        
        return list(self.session.scalars(stmt).unique().all())

    def get_por_especialidad(self, especialidad_id: int) -> List[Medico]:
        """
        Obtiene médicos activos que tienen la especialidad dada.
        
        Args:
            especialidad_id: ID de la especialidad
        
        Returns:
            Lista de médicos con esa especialidad
        """
        stmt = select(Medico).join(
            Medico.especialidades
        ).where(
            Medico.activo == True,  # noqa: E712
            Medico.especialidades.any(id=especialidad_id)
        ).options(joinedload(Medico.especialidades))
        
        return list(self.session.scalars(stmt).unique().all())

    def get_con_turnos_pendientes(self, medico_id: int) -> bool:
        """
        Verifica si el médico tiene turnos pendientes o confirmados.
        
        Args:
            medico_id: ID del médico
        
        Returns:
            True si tiene turnos pendientes, False en caso contrario
        """
        medico = self.get_by_id(medico_id)
        if medico is None:
            return False
        
        return medico.tiene_turnos_pendientes()
