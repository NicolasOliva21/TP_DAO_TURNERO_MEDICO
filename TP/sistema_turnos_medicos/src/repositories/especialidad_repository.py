"""Repositorio para la entidad Especialidad."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.especialidad import Especialidad
from src.repositories.base_repository import BaseRepository


class EspecialidadRepository(BaseRepository[Especialidad]):
    """Repositorio específico para Especialidades."""

    def __init__(self, session: Session):
        super().__init__(session, Especialidad)

    def get_by_nombre(self, nombre: str) -> Optional[Especialidad]:
        """Busca especialidad por nombre exacto (solo activas)."""
        stmt = select(Especialidad).where(
            Especialidad.nombre == nombre,
            Especialidad.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def exists_nombre(self, nombre: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una especialidad activa con el nombre dado.
        
        Args:
            nombre: Nombre a verificar
            exclude_id: ID de especialidad a excluir (útil para actualizaciones)
        """
        stmt = select(Especialidad).where(
            Especialidad.nombre == nombre,
            Especialidad.activo == True  # noqa: E712
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Especialidad.id != exclude_id)
        
        return self.session.scalar(stmt) is not None

    def buscar(self, texto: str) -> List[Especialidad]:
        """
        Búsqueda por nombre o descripción.
        
        Args:
            texto: Texto a buscar
        
        Returns:
            Lista de especialidades que coinciden con la búsqueda
        """
        texto_lower = f"%{texto.lower()}%"
        
        stmt = select(Especialidad).where(
            Especialidad.activo == True,  # noqa: E712
            (Especialidad.nombre.ilike(texto_lower) | 
             Especialidad.descripcion.ilike(texto_lower))
        )
        
        return list(self.session.scalars(stmt).all())

    def tiene_medicos_o_turnos(self, especialidad_id: int) -> bool:
        """
        Verifica si la especialidad tiene médicos o turnos asociados.
        
        Args:
            especialidad_id: ID de la especialidad
        
        Returns:
            True si tiene médicos o turnos, False en caso contrario
        """
        especialidad = self.get_by_id(especialidad_id)
        if especialidad is None:
            return False
        
        return especialidad.tiene_medicos_o_turnos()
