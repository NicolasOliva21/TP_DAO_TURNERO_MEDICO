from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from typing import List, Optional

class DoctorRepo:
    @staticmethod
    def list(db: Session) -> List[Doctor]:
        return db.query(Doctor).order_by(Doctor.apellido, Doctor.nombre).all()

    @staticmethod
    def create(db: Session, **data) -> Doctor:
        obj = Doctor(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def get(db: Session, did: int) -> Optional[Doctor]:
        return db.get(Doctor, did)

    @staticmethod
    def update(db: Session, did: int, **data) -> Doctor:
        obj = db.get(Doctor, did)
        for k, v in data.items(): setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def set_estado(db: Session, did: int, activo: bool) -> None:
        obj = db.get(Doctor, did); obj.activo = activo
        db.commit()
