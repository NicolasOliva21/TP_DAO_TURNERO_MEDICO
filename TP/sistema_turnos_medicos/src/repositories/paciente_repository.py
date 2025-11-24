"""Repositorio para la entidad Paciente."""
from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.domain.paciente import Paciente
from src.repositories.base_repository import BaseRepository


class PacienteRepository(BaseRepository[Paciente]):
    """Repositorio específico para Pacientes."""

    def __init__(self, session: Session):
        super().__init__(session, Paciente)

    def get_by_dni(self, dni: str) -> Optional[Paciente]:
        """Busca paciente por DNI (solo activos)."""
        stmt = select(Paciente).where(
            Paciente.dni == dni,
            Paciente.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def get_by_email(self, email: str) -> Optional[Paciente]:
        """Busca paciente por email (solo activos)."""
        stmt = select(Paciente).where(
            Paciente.email == email.lower(),
            Paciente.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def exists_dni(self, dni: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un paciente activo con el DNI dado.
        
        Args:
            dni: DNI a verificar
            exclude_id: ID de paciente a excluir (útil para actualizaciones)
        """
        stmt = select(Paciente).where(
            Paciente.dni == dni,
            Paciente.activo == True  # noqa: E712
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Paciente.id != exclude_id)
        
        return self.session.scalar(stmt) is not None

    def exists_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un paciente activo con el email dado.
        
        Args:
            email: Email a verificar
            exclude_id: ID de paciente a excluir (útil para actualizaciones)
        """
        stmt = select(Paciente).where(
            Paciente.email == email.lower(),
            Paciente.activo == True  # noqa: E712
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Paciente.id != exclude_id)
        
        return self.session.scalar(stmt) is not None

    def buscar(self, texto: str) -> List[Paciente]:
        """
        Búsqueda por nombre, apellido o DNI.
        
        Args:
            texto: Texto a buscar
        
        Returns:
            Lista de pacientes que coinciden con la búsqueda
        """
        texto_lower = f"%{texto.lower()}%"
        
        stmt = select(Paciente).where(
            Paciente.activo == True,  # noqa: E712
            or_(
                Paciente.nombre.ilike(texto_lower),
                Paciente.apellido.ilike(texto_lower),
                Paciente.dni.like(f"%{texto}%")
            )
        )
        
        return list(self.session.scalars(stmt).all())

    def get_con_turnos_futuros(self, paciente_id: int) -> bool:
        """
        Verifica si el paciente tiene turnos futuros activos.
        
        Args:
            paciente_id: ID del paciente
        
        Returns:
            True si tiene turnos futuros, False en caso contrario
        """
        paciente = self.get_by_id(paciente_id)
        if paciente is None:
            return False
        
        return paciente.tiene_turnos_futuros()
