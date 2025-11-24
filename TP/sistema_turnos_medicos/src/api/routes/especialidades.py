"""
Rutas para gestión de especialidades.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas import EspecialidadResponse
from src.api.dependencies import get_uow
from src.repositories.unit_of_work import UnitOfWork

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])


@router.get("/", response_model=List[EspecialidadResponse])
def listar_especialidades(
    skip: int = 0,
    limit: int = 100,
    uow: UnitOfWork = Depends(get_uow)
):
    """Lista todas las especialidades activas."""
    especialidades = uow.especialidades.get_all(skip=skip, limit=limit)
    return especialidades


@router.get("/{especialidad_id}", response_model=EspecialidadResponse)
def obtener_especialidad(
    especialidad_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Obtiene una especialidad por ID."""
    especialidad = uow.especialidades.get_by_id(especialidad_id)
    if not especialidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Especialidad con ID {especialidad_id} no encontrada"
        )
    return especialidad
