"""
Rutas para gestión de turnos.
Endpoint principal del sistema.
"""
from typing import List, Dict
from datetime import datetime, timedelta, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.api.schemas import (
    TurnoResponse, TurnoCreate, TurnoUpdate, 
    SuccessResponse, HorarioDisponibleResponse
)
from src.api.dependencies import get_uow
from src.repositories.unit_of_work import UnitOfWork
from src.services.turno_service import TurnoService
from src.utils.exceptions import *

router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.get("/", response_model=List[TurnoResponse])
def listar_turnos(
    fecha_desde: datetime = None,
    fecha_hasta: datetime = None,
    id_paciente: int = None,
    id_medico: int = None,
    codigo_estado: str = None,
    skip: int = 0,
    limit: int = 100,
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Lista turnos con filtros opcionales.
    Útil para ver la agenda completa o filtrada.
    """
    # Aplicar filtros básicos
    query = uow.session.query(uow.turnos.model)
    
    if fecha_desde:
        query = query.filter(uow.turnos.model.fecha_hora >= fecha_desde)
    if fecha_hasta:
        query = query.filter(uow.turnos.model.fecha_hora <= fecha_hasta)
    if id_paciente:
        query = query.filter(uow.turnos.model.id_paciente == id_paciente)
    if id_medico:
        query = query.filter(uow.turnos.model.id_medico == id_medico)
    if codigo_estado:
        estado = uow.estados_turno.get_by_codigo(codigo_estado)
        if estado:
            query = query.filter(uow.turnos.model.id_estado == estado.id)
    
    query = query.filter(uow.turnos.model.activo == True)
    turnos = query.offset(skip).limit(limit).all()
    
    return turnos


@router.get("/paciente/{paciente_id}", response_model=List[TurnoResponse])
def obtener_turnos_paciente(
    paciente_id: int,
    solo_futuros: bool = True,
    uow: UnitOfWork = Depends(get_uow)
):
    """Obtiene todos los turnos de un paciente."""
    paciente = uow.pacientes.get_by_id(paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paciente con ID {paciente_id} no encontrado"
        )
    
    if solo_futuros:
        turnos = uow.turnos.get_turnos_futuros_paciente(paciente_id)
    else:
        query = uow.session.query(uow.turnos.model).filter(
            uow.turnos.model.id_paciente == paciente_id,
            uow.turnos.model.activo == True
        )
        turnos = query.all()
    
    return turnos


@router.get("/medico/{medico_id}", response_model=List[TurnoResponse])
def obtener_turnos_medico(
    medico_id: int,
    fecha: date = None,
    uow: UnitOfWork = Depends(get_uow)
):
    """Obtiene todos los turnos de un médico, opcionalmente para una fecha específica."""
    medico = uow.medicos.get_by_id(medico_id)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico con ID {medico_id} no encontrado"
        )
    
    if fecha:
        turnos = uow.turnos.get_turnos_medico_fecha(medico_id, fecha)
    else:
        query = uow.session.query(uow.turnos.model).filter(
            uow.turnos.model.id_medico == medico_id,
            uow.turnos.model.activo == True
        )
        turnos = query.all()
    
    return turnos


@router.get("/disponibles", response_model=List[HorarioDisponibleResponse])
def obtener_horarios_disponibles(
    id_medico: int = Query(..., description="ID del médico"),
    fecha: date = Query(..., description="Fecha para buscar disponibilidad"),
    duracion: int = Query(30, description="Duración del turno en minutos"),
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Obtiene los horarios disponibles de un médico para una fecha específica.
    Este es el endpoint clave para la reserva eficiente de turnos.
    """
    # Validar que la fecha no sea en el pasado
    if fecha < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden solicitar turnos en fechas pasadas"
        )
    
    try:
        turno_service = TurnoService(uow)
        horarios = turno_service.obtener_horarios_disponibles(id_medico, fecha, duracion)
        
        return [
            HorarioDisponibleResponse(fecha_hora=h, disponible=True)
            for h in horarios
        ]
        
    except DisponibilidadException as e:
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener horarios: {str(e)}"
        )


@router.get("/calendario/{id_medico}")
def obtener_calendario_disponibilidad(
    id_medico: int,
    dias: int = Query(14, description="Cantidad de días a mostrar desde hoy"),
    duracion: int = Query(30, description="Duración del turno en minutos"),
    uow: UnitOfWork = Depends(get_uow)
) -> Dict[str, List[str]]:
    """
    Obtiene un calendario con todos los horarios disponibles del médico
    para los próximos N días. Formato: {fecha: [horarios]}
    """
    try:
        turno_service = TurnoService(uow)
        calendario = {}
        fecha_actual = date.today()
        
        for i in range(dias):
            fecha = fecha_actual + timedelta(days=i)
            
            try:
                horarios = turno_service.obtener_horarios_disponibles(id_medico, fecha, duracion)
                if horarios:
                    # Convertir a string ISO format
                    calendario[fecha.isoformat()] = [
                        h.isoformat() for h in horarios
                    ]
            except DisponibilidadException:
                # El médico no atiende ese día
                continue
        
        return calendario
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener calendario: {str(e)}"
        )


@router.get("/{turno_id}", response_model=TurnoResponse)
def obtener_turno(
    turno_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Obtiene un turno específico por ID."""
    turno = uow.turnos.get_by_id(turno_id)
    if not turno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Turno con ID {turno_id} no encontrado"
        )
    return turno


@router.post("/", response_model=TurnoResponse, status_code=status.HTTP_201_CREATED)
def crear_turno(
    turno_data: TurnoCreate,
    uow: UnitOfWork = Depends(get_uow)
):
    """
    Crea un nuevo turno.
    Valida disponibilidad, solapamiento y todas las reglas de negocio.
    """
    try:
        turno_service = TurnoService(uow)
        
        turno = turno_service.crear_turno(
            id_paciente=turno_data.id_paciente,
            id_medico=turno_data.id_medico,
            id_especialidad=turno_data.id_especialidad,
            fecha_hora=turno_data.fecha_hora,
            duracion_minutos=turno_data.duracion_minutos,
            motivo=turno_data.motivo
        )
        
        uow.commit()
        return turno
        
    except (
        FechaPasadaException,
        DisponibilidadException,
        SolapamientoTurnoException,
        EspecialidadInvalidaException,
        PacienteNoEncontradoException,
        MedicoNoEncontradoException,
        EspecialidadNoEncontradaException
    ) as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear turno: {str(e)}"
        )


@router.patch("/{turno_id}", response_model=TurnoResponse)
def actualizar_turno(
    turno_id: int,
    turno_update: TurnoUpdate,
    uow: UnitOfWork = Depends(get_uow)
):
    """Actualiza el motivo o estado de un turno."""
    try:
        turno = uow.turnos.get_by_id(turno_id)
        if not turno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Turno con ID {turno_id} no encontrado"
            )
        
        if turno_update.motivo is not None:
            turno.motivo = turno_update.motivo
        
        if turno_update.codigo_estado is not None:
            estado = uow.estados_turno.get_by_codigo(turno_update.codigo_estado)
            if not estado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estado '{turno_update.codigo_estado}' no válido"
                )
            turno.id_estado = estado.id
        
        uow.commit()
        return turno
        
    except HTTPException:
        raise
    except Exception as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar turno: {str(e)}"
        )


@router.post("/{turno_id}/confirmar", response_model=SuccessResponse)
def confirmar_turno(
    turno_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Confirma un turno pendiente."""
    try:
        turno = uow.turnos.get_by_id(turno_id)
        if not turno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Turno con ID {turno_id} no encontrado"
            )
        
        turno.confirmar()
        uow.commit()
        
        return SuccessResponse(message="Turno confirmado exitosamente")
        
    except Exception as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al confirmar turno: {str(e)}"
        )


@router.post("/{turno_id}/cancelar", response_model=SuccessResponse)
def cancelar_turno(
    turno_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Cancela un turno."""
    try:
        turno = uow.turnos.get_by_id(turno_id)
        if not turno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Turno con ID {turno_id} no encontrado"
            )
        
        turno.cancelar()
        uow.commit()
        
        return SuccessResponse(message="Turno cancelado exitosamente")
        
    except TurnoCanceladoException as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cancelar turno: {str(e)}"
        )


@router.delete("/{turno_id}", response_model=SuccessResponse)
def eliminar_turno(
    turno_id: int,
    uow: UnitOfWork = Depends(get_uow)
):
    """Realiza soft delete de un turno."""
    try:
        turno = uow.turnos.get_by_id(turno_id)
        if not turno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Turno con ID {turno_id} no encontrado"
            )
        
        uow.turnos.delete(turno_id)
        uow.commit()
        
        return SuccessResponse(message="Turno eliminado correctamente")
        
    except Exception as e:
        uow.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar turno: {str(e)}"
        )
