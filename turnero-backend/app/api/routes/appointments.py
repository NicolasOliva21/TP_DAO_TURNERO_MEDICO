from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.services.appointment_service import AppointmentService
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/turnos", tags=["turnos"])

@router.get("", response_model=List[AppointmentOut])
def list_turnos(medico_id: Optional[int] = None, desde: Optional[str] = None, hasta: Optional[str] = None,
                db: Session = Depends(get_db), _=Depends(get_current_user)):
    return AppointmentService.list(db, medico_id, desde, hasta)

@router.post("", response_model=AppointmentOut)
def create_turno(payload: AppointmentCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    try:
        return AppointmentService.create(db, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{tid}", response_model=AppointmentOut)
def update_turno(tid: int, payload: AppointmentUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    try:
        return AppointmentService.update(db, tid, payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{tid}/cancelar")
def cancelar_turno(tid: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    AppointmentService.cancelar(db, tid)
    return {"ok": True}

@router.post("/{tid}/atender")
def atender_turno(tid: int, receta_url: str | None = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    AppointmentService.atender(db, tid, receta_url)
    return {"ok": True}

@router.get("/disponibles")
def turnos_disponibles(medico_id: int, fecha: str,
                       duracion_min: int = 30, inicio: str = "09:00", fin: str = "17:00",
                       db: Session = Depends(get_db), _=Depends(get_current_user)):
    # fecha = "YYYY-MM-DD"
    try:
        return AppointmentService.disponibles(db, medico_id, fecha, duracion_min, inicio, fin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
