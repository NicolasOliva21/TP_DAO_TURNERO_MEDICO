from sqlalchemy.orm import Session
from app.repositories.specialty_repo import SpecialtyRepo

class SpecialtyService:
    @staticmethod
    def list(db: Session): return SpecialtyRepo.list(db)
    @staticmethod
    def create(db: Session, data: dict): return SpecialtyRepo.create(db, **data)
    @staticmethod
    def update(db: Session, sid: int, data: dict): return SpecialtyRepo.update(db, sid, **data)
    @staticmethod
    def set_estado(db: Session, sid: int, activa: bool): return SpecialtyRepo.set_estado(db, sid, activa)
