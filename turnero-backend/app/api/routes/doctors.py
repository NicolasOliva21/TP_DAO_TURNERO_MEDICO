from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from app.services.doctor_service import DoctorService
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/medicos", tags=["medicos"])

@router.get("", response_model=List[DoctorOut])
def list_doctors(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return DoctorService.list(db)

@router.post("", response_model=DoctorOut)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return DoctorService.create(db, payload.model_dump())

@router.put("/{did}", response_model=DoctorOut)
def update_doctor(did: int, payload: DoctorUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return DoctorService.update(db, did, payload.model_dump(exclude_unset=True))

@router.patch("/{did}/estado")
def toggle_doctor(did: int, activo: bool, db: Session = Depends(get_db), _=Depends(get_current_user)):
    DoctorService.set_estado(db, did, activo)
    return {"ok": True}
