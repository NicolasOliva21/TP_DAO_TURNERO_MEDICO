"""
Repositorio base con operaciones CRUD genéricas.
Patrón Template Method para reutilización de código.
"""
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Repositorio base con operaciones CRUD genéricas.
    Todas las entidades heredan este comportamiento.
    """

    def __init__(self, session: Session, model_class: Type[T]):
        """
        Args:
            session: Sesión de SQLAlchemy
            model_class: Clase del modelo de dominio
        """
        self.session = session
        self.model_class = model_class

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Obtiene una entidad por su ID (solo activas)."""
        stmt = select(self.model_class).where(
            self.model_class.id == entity_id,
            self.model_class.activo == True  # noqa: E712
        )
        return self.session.scalar(stmt)

    def get_by_id_incluye_inactivos(self, entity_id: int) -> Optional[T]:
        """Obtiene una entidad por su ID (incluye inactivas)."""
        stmt = select(self.model_class).where(self.model_class.id == entity_id)
        return self.session.scalar(stmt)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todas las entidades activas."""
        stmt = select(self.model_class).where(
            self.model_class.activo == True  # noqa: E712
        ).offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_all_incluye_inactivos(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene todas las entidades (incluye inactivas)."""
        stmt = select(self.model_class).offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())

    def add(self, entity: T) -> T:
        """
        Agrega una nueva entidad a la sesión.
        No hace commit automático (manejo por Unit of Work).
        """
        self.session.add(entity)
        self.session.flush()  # Para obtener el ID generado
        return entity

    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.
        No hace commit automático (manejo por Unit of Work).
        """
        merged_entity = self.session.merge(entity)
        self.session.flush()
        return merged_entity

    def delete(self, entity: T) -> None:
        """
        Baja lógica de la entidad (soft delete).
        No hace commit automático.
        """
        entity.soft_delete()
        self.session.flush()

    def restore(self, entity: T) -> T:
        """
        Restaura una entidad dada de baja.
        No hace commit automático.
        """
        entity.restore()
        self.session.flush()
        return entity

    def delete_permanently(self, entity: T) -> None:
        """
        Baja física de la entidad (hard delete).
        Usar con precaución - pérdida de datos.
        """
        self.session.delete(entity)
        self.session.flush()

    def exists(self, entity_id: int) -> bool:
        """Verifica si existe una entidad activa con el ID dado."""
        return self.get_by_id(entity_id) is not None

    def count(self) -> int:
        """Cuenta las entidades activas."""
        stmt = select(self.model_class).where(
            self.model_class.activo == True  # noqa: E712
        )
        return len(list(self.session.scalars(stmt).all()))
