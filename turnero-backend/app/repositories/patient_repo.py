from sqlalchemy.orm import Session
from app.models.patient import Patient
from typing import List, Optional

class PatientRepo:
    @staticmethod
    def list(db: Session) -> List[Patient]:
        return db.query(Patient).order_by(Patient.apellido, Patient.nombre).all()

    @staticmethod
    def create(db: Session, **data) -> Patient:
        obj = Patient(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def get(db: Session, pid: int) -> Optional[Patient]:
        return db.get(Patient, pid)

    @staticmethod
    def update(db: Session, pid: int, **data) -> Patient:
        obj = db.get(Patient, pid)
        for k, v in data.items(): setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def set_estado(db: Session, pid: int, activo: bool) -> None:
        obj = db.get(Patient, pid); obj.activo = activo
        db.commit()
