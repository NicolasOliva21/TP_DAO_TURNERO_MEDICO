from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.appointment import Appointment, TurnoEstado
from typing import List, Optional

class AppointmentRepo:
    @staticmethod
    def list(db: Session, medico_id: int | None = None, desde: str | None = None, hasta: str | None = None) -> List[Appointment]:
        stmt = select(Appointment)
        if medico_id:
            stmt = stmt.where(Appointment.medico_id == medico_id)
        if desde:
            stmt = stmt.where(Appointment.fecha >= desde)
        if hasta:
            stmt = stmt.where(Appointment.fecha <= hasta)
        stmt = stmt.order_by(Appointment.fecha)
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def create(db: Session, **data) -> Appointment:
        obj = Appointment(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def get(db: Session, tid: int) -> Optional[Appointment]:
        return db.get(Appointment, tid)

    @staticmethod
    def update(db: Session, tid: int, **data) -> Appointment:
        obj = db.get(Appointment, tid)
        for k, v in data.items(): setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    @staticmethod
    def cancel(db: Session, tid: int):
        obj = db.get(Appointment, tid)
        obj.estado = TurnoEstado.Cancelado
        db.commit()

    @staticmethod
    def atender(db: Session, tid: int, receta_url: str | None = None):
        obj = db.get(Appointment, tid)
        obj.estado = TurnoEstado.Atendido
        if receta_url: obj.receta_url = receta_url
        db.commit()

    @staticmethod
    def overlaps(db: Session, medico_id: int, inicio: str, fin: str) -> bool:
        # Solape si: (A.start < B.end) AND (B.start < A.end)
        stmt = select(Appointment).where(
            and_(
                Appointment.medico_id == medico_id,
                Appointment.estado != TurnoEstado.Cancelado,
                Appointment.fecha < fin,
                inicio < Appointment.fecha  # comparar strings ISO YYYY-MM-DDTHH:MM funciona lexical
            )
        )
        return db.execute(stmt).first() is not None
