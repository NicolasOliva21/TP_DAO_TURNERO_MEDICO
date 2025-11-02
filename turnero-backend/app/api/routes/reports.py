from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.appointment_service import AppointmentService
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/reportes", tags=["reportes"])

@router.get("/turnos-medico")
def rpt_turnos_medico(desde: Optional[str] = None, hasta: Optional[str] = None,
                      db: Session = Depends(get_db), _=Depends(get_current_user)):
    return AppointmentService.reportes_por_medico(db, desde, hasta)

@router.get("/turnos-especialidad")
def rpt_turnos_especialidad(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return AppointmentService.reportes_por_especialidad(db)

@router.get("/resumen")
def resumen(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return AppointmentService.resumen(db)
