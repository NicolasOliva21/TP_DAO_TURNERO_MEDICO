"""
Rutas para gestión de médicos.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas import MedicoResponse, MedicoListResponse, DisponibilidadResponse
from src.api.dependencies import get_uow
from src.repositories.unit_of_work import UnitOfWork

router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.get("/", response_model=List[MedicoListResponse])
def listar_medicos(
    skip: int = 0,
    limit: int = 100,
    uow: UnitOfWork = Depends(get_uow)
):
    """Lista todos los médicos activos."""
    medicos = uow.medicos.get_all(skip=skip, limit=limit)
    return [
        MedicoListResponse(
            id=m.id,
            matricula=m.matricula,
            nombre=m.nombre,
            apellido=m.apellido,
            nombre_completo=m.nombre_completo
        )
        for m in medicos
    ]


@router.get("/{medico_id}", response_model=MedicoResponse)
def obtener_medico(
    medico_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Obtiene un médico por ID con sus especialidades."""
    medico = uow.medicos.get_by_id(medico_id)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico con ID {medico_id} no encontrado"
        )
    return medico


@router.get("/especialidad/{especialidad_id}", response_model=List[MedicoListResponse])
def listar_medicos_por_especialidad(
    especialidad_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Lista médicos que tienen una especialidad específica."""
    medicos = uow.medicos.get_por_especialidad(especialidad_id)
    return [
        MedicoListResponse(
            id=m.id,
            matricula=m.matricula,
            nombre=m.nombre,
            apellido=m.apellido,
            nombre_completo=m.nombre_completo
        )
        for m in medicos
    ]


@router.get("/{medico_id}/disponibilidades", response_model=List[DisponibilidadResponse])
def obtener_disponibilidades_medico(
    medico_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Obtiene las disponibilidades semanales de un médico."""
    medico = uow.medicos.get_by_id(medico_id)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico con ID {medico_id} no encontrado"
        )
    
    disponibilidades = uow.disponibilidades.get_por_medico(medico_id)
    return disponibilidades
