from sqlalchemy.orm import Session
from app.repositories.doctor_repo import DoctorRepo

class DoctorService:
    @staticmethod
    def list(db: Session): return DoctorRepo.list(db)
    @staticmethod
    def create(db: Session, data: dict): return DoctorRepo.create(db, **data)
    @staticmethod
    def update(db: Session, did: int, data: dict): return DoctorRepo.update(db, did, **data)
    @staticmethod
    def set_estado(db: Session, did: int, activo: bool): return DoctorRepo.set_estado(db, did, activo)
