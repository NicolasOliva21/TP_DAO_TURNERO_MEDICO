from sqlalchemy.orm import Session
from app.repositories.patient_repo import PatientRepo

class PatientService:
    @staticmethod
    def list(db: Session): return PatientRepo.list(db)
    @staticmethod
    def create(db: Session, data: dict): return PatientRepo.create(db, **data)
    @staticmethod
    def update(db: Session, pid: int, data: dict): return PatientRepo.update(db, pid, **data)
    @staticmethod
    def set_estado(db: Session, pid: int, activo: bool): return PatientRepo.set_estado(db, pid, activo)
