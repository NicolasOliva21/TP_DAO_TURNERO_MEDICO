"""
Rutas para gestión de especialidades.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas import EspecialidadResponse, EspecialidadCreate, EspecialidadUpdate
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


@router.post("/", response_model=EspecialidadResponse, status_code=status.HTTP_201_CREATED)
def crear_especialidad(
    especialidad: EspecialidadCreate,
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Crea una nueva especialidad.
    Valida que el nombre no exista.
    """
    # Verificar que no exista otra especialidad con el mismo nombre
    especialidades_existentes = uow.especialidades.get_all()
    if any(e.nombre.lower() == especialidad.nombre.lower() for e in especialidades_existentes):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una especialidad con ese nombre"
        )
    
    # Crear especialidad
    from src.domain.especialidad import Especialidad
    nueva_especialidad = Especialidad(
        nombre=especialidad.nombre,
        descripcion=especialidad.descripcion,
        activo=True
    )
    
    uow.especialidades.add(nueva_especialidad)
    uow.commit()
    
    return nueva_especialidad


@router.put("/{especialidad_id}", response_model=EspecialidadResponse)
def actualizar_especialidad(
    especialidad_id: int,
    especialidad_update: EspecialidadUpdate,
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Actualiza una especialidad existente.
    Valida que el nuevo nombre no exista.
    """
    especialidad = uow.especialidades.get_by_id(especialidad_id)
    if not especialidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Especialidad con ID {especialidad_id} no encontrada"
        )
    
    # Validar nombre único si se modifica
    if especialidad_update.nombre and especialidad_update.nombre.lower() != especialidad.nombre.lower():
        especialidades_existentes = uow.especialidades.get_all()
        if any(e.id != especialidad_id and e.nombre.lower() == especialidad_update.nombre.lower() 
               for e in especialidades_existentes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otra especialidad con ese nombre"
            )
        especialidad.nombre = especialidad_update.nombre
    
    # Actualizar descripción si se proporciona
    if especialidad_update.descripcion is not None:
        especialidad.descripcion = especialidad_update.descripcion
    
    uow.commit()
    return especialidad


@router.delete("/{especialidad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_especialidad(
    especialidad_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Elimina (baja lógica) una especialidad.
    Valida que no tenga médicos asociados.
    """
    especialidad = uow.especialidades.get_by_id(especialidad_id)
    if not especialidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Especialidad con ID {especialidad_id} no encontrada"
        )
    
    # Verificar que no tenga médicos asociados
    medicos = uow.medicos.get_por_especialidad(especialidad_id)
    if medicos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar la especialidad porque tiene {len(medicos)} médico(s) asociado(s)"
        )
    
    uow.especialidades.delete(especialidad)
    uow.commit()
