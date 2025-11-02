from sqlalchemy.orm import Session
from app.models.specialty import Specialty
from typing import List, Optional

class SpecialtyRepo:
    @staticmethod
    def list(db: Session) -> List[Specialty]:
        return db.query(Specialty).order_by(Specialty.nombre).all()

    @staticmethod
    def create(db: Session, **data) -> Specialty:
        obj = Specialty(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def get(db: Session, sid: int) -> Optional[Specialty]:
        return db.get(Specialty, sid)

    @staticmethod
    def update(db: Session, sid: int, **data) -> Specialty:
        obj = db.get(Specialty, sid)
        for k, v in data.items(): setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def set_estado(db: Session, sid: int, activa: bool) -> None:
        obj = db.get(Specialty, sid); obj.activa = activa
        db.commit()
