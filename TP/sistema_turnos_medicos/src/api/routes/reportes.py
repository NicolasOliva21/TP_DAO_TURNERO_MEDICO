from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date

from src.services.reporte_service import ReporteService
from src.api.schemas import (
    TurnoReporteResponse,
    EspecialidadReporteResponse,
    PacienteReporteResponse,
    AsistenciaReporteResponse
)

router = APIRouter(prefix="/reportes", tags=["Reportes"])
reporte_service = ReporteService()

@router.get("/turnos-medico", response_model=List[TurnoReporteResponse])
def get_turnos_por_medico(
    fecha_inicio: date,
    fecha_fin: date,
    medico_id: Optional[int] = None,
    especialidad_id: Optional[int] = None
):
    """
    Obtiene el listado de turnos en un rango de fechas, con filtros opcionales.
    """
    return reporte_service.get_turnos_por_medico(fecha_inicio, fecha_fin, medico_id, especialidad_id)

@router.get("/turnos-especialidad", response_model=List[EspecialidadReporteResponse])
def get_turnos_por_especialidad(
    fecha_inicio: date,
    fecha_fin: date,
    medico_id: Optional[int] = None,
    especialidad_id: Optional[int] = None
):
    """
    Cuenta la cantidad de turnos por especialidad en un rango de fechas, con filtros opcionales.
    """
    return reporte_service.get_turnos_por_especialidad(fecha_inicio, fecha_fin, medico_id, especialidad_id)

@router.get("/pacientes-atendidos", response_model=List[PacienteReporteResponse])
def get_pacientes_atendidos(
    fecha_inicio: date,
    fecha_fin: date,
    medico_id: Optional[int] = None,
    especialidad_id: Optional[int] = None
):
    """
    Obtiene los pacientes atendidos en un rango de fechas.
    """
    return reporte_service.get_pacientes_atendidos(fecha_inicio, fecha_fin, medico_id, especialidad_id)

@router.get("/asistencia", response_model=AsistenciaReporteResponse)
def get_estadisticas_asistencia(
    fecha_inicio: date,
    fecha_fin: date,
    medico_id: Optional[int] = None,
    especialidad_id: Optional[int] = None
):
    """
    Calcula la cantidad de asistencias e inasistencias con filtros opcionales.
    """
    return reporte_service.get_estadisticas_asistencia(fecha_inicio, fecha_fin, medico_id, especialidad_id)
