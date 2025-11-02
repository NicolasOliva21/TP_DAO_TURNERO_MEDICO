from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.patient import PatientCreate, PatientUpdate, PatientOut
from app.services.patient_service import PatientService
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.get("", response_model=List[PatientOut])
def list_pacientes(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return PatientService.list(db)

@router.post("", response_model=PatientOut)
def create_paciente(payload: PatientCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return PatientService.create(db, payload.model_dump())

@router.put("/{pid}", response_model=PatientOut)
def update_paciente(pid: int, payload: PatientUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return PatientService.update(db, pid, payload.model_dump(exclude_unset=True))

@router.patch("/{pid}/estado")
def toggle_paciente(pid: int, activo: bool, db: Session = Depends(get_db), _=Depends(get_current_user)):
    PatientService.set_estado(db, pid, activo)
    return {"ok": True}
