from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.repositories.appointment_repo import AppointmentRepo
from app.models.appointment import TurnoEstado

FMT = "%Y-%m-%dT%H:%M"

def _end_time(start_iso: str, dur_min: int) -> str:
    dt = datetime.strptime(start_iso, FMT) + timedelta(minutes=dur_min)
    return dt.strftime(FMT)

class AppointmentService:
    @staticmethod
    def list(db: Session, medico_id: int | None, desde: str | None, hasta: str | None):
        return AppointmentRepo.list(db, medico_id, desde, hasta)

    @staticmethod
    def create(db: Session, data: dict):
        inicio = data["fecha"]
        fin = _end_time(inicio, data.get("duracion_min", 30))
        if AppointmentRepo.overlaps(db, data["medico_id"], inicio, fin):
            raise ValueError("El médico ya tiene un turno solapado en ese horario")
        return AppointmentRepo.create(db, **data)

    @staticmethod
    def update(db: Session, tid: int, data: dict):
        # Si reprograma, validar solape
        if "fecha" in data or "duracion_min" in data:
            existing = AppointmentRepo.get(db, tid)
            inicio = data.get("fecha", existing.fecha)
            dur = data.get("duracion_min", existing.duracion_min)
            fin = _end_time(inicio, dur)
            if AppointmentRepo.overlaps(db, existing.medico_id, inicio, fin):
                raise ValueError("El médico ya tiene un turno solapado en ese horario")
        return AppointmentRepo.update(db, tid, **data)

    @staticmethod
    def cancelar(db: Session, tid: int):
        return AppointmentRepo.cancel(db, tid)

    @staticmethod
    def atender(db: Session, tid: int, receta_url: str | None):
        return AppointmentRepo.atender(db, tid, receta_url)

    @staticmethod
    def resumen(db: Session):
        # Pequeño resumen para dashboard
        from app.models.patient import Patient
        from app.models.doctor import Doctor
        from sqlalchemy import select, func
        from app.models.appointment import Appointment
        total_pacientes = db.scalar(select(func.count(Patient.id))) or 0
        total_medicos = db.scalar(select(func.count(Doctor.id))) or 0
        # turnos hoy (fecha empieza por YYYY-MM-DD de hoy)
        today_prefix = datetime.now().strftime("%Y-%m-%d")
        turnos_hoy = db.scalar(
            select(func.count(Appointment.id)).where(Appointment.fecha.like(f"{today_prefix}%"),
                                                     Appointment.estado != TurnoEstado.Cancelado)
        ) or 0
        return {"pacientes": total_pacientes, "medicos": total_medicos, "turnos_hoy": turnos_hoy}

    @staticmethod
    def reportes_por_medico(db: Session, desde: str | None, hasta: str | None):
        from sqlalchemy import select, func
        from app.models.appointment import Appointment
        from app.models.doctor import Doctor
        stmt = select(Doctor.apellido, Doctor.nombre, func.count(Appointment.id))\
            .join(Appointment, Appointment.medico_id == Doctor.id, isouter=True)
        if desde: stmt = stmt.where((Appointment.fecha >= desde) | (Appointment.id == None))
        if hasta: stmt = stmt.where((Appointment.fecha <= hasta) | (Appointment.id == None))
        stmt = stmt.group_by(Doctor.id)
        rows = db.execute(stmt).all()
        return [{"medico": f"{a}, {n}", "fecha": f"{desde or '-'}→{hasta or '-'}", "total": int(t or 0)} for a, n, t in rows]

    @staticmethod
    def reportes_por_especialidad(db: Session):
        from sqlalchemy import select, func
        from app.models.appointment import Appointment
        from app.models.specialty import Specialty
        stmt = select(Specialty.nombre, func.count(Appointment.id))\
            .join(Appointment, Appointment.especialidad_id == Specialty.id, isouter=True)\
            .group_by(Specialty.id)
        rows = db.execute(stmt).all()
        return [{"especialidad": n, "total": int(t or 0)} for n, t in rows]

# --- NUEVO: slots disponibles por médico/fecha ---
from typing import List, Dict

def _to_dt(date_iso: str, hm: str) -> datetime:
    # date_iso: "YYYY-MM-DD", hm: "HH:MM"
    return datetime.strptime(f"{date_iso}T{hm}", FMT)

class AppointmentService:
    # ... (resto de la clase queda igual)

    @staticmethod
    def disponibles(db: Session, medico_id: int, fecha: str,
                    duracion_min: int = 30, inicio: str = "09:00", fin: str = "17:00") -> List[Dict]:
        """
        Genera slots de [inicio, fin) para la fecha indicada y filtra los que se solapan con
        turnos ya reservados (no cancelados) del médico.
        Responde: [{ "iso": "YYYY-MM-DDTHH:MM", "inicio": "HH:MM", "fin": "HH:MM" }, ...]
        """
        # 1) ventana laboral del día
        day_start = _to_dt(fecha, inicio)
        day_end   = _to_dt(fecha, fin)

        # 2) turnos existentes ese día (no cancelados)
        desde = day_start.strftime(FMT)
        hasta = day_end.strftime(FMT)
        existentes = AppointmentRepo.list(db, medico_id=medico_id, desde=desde, hasta=hasta)

        # transformar a rangos datetime
        busy: List[tuple[datetime, datetime]] = []
        for ap in existentes:
            if ap.estado == TurnoEstado.Cancelado:
                continue
            ap_start = datetime.strptime(ap.fecha, FMT)
            ap_end   = ap_start + timedelta(minutes=ap.duracion_min)
            busy.append((ap_start, ap_end))

        # 3) generar slots
        cur = day_start
        slots: List[Dict] = []
        step = timedelta(minutes=duracion_min)
        while cur + step <= day_end:
            s_start = cur
            s_end   = cur + step
            # si NO se solapa con ningún turno => disponible
            overlap = any((s_start < e_end and ap_start < s_end) for ap_start, e_end in busy)
            if not overlap:
                slots.append({
                    "iso": s_start.strftime(FMT),
                    "inicio": s_start.strftime("%H:%M"),
                    "fin": s_end.strftime("%H:%M")
                })
            cur += step

        return slots

