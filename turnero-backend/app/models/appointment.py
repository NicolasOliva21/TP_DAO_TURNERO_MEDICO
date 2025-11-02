from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class TurnoEstado(str, enum.Enum):
    Reservado = "Reservado"
    Cancelado = "Cancelado"
    Reprogramado = "Reprogramado"
    Atendido = "Atendido"

class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="RESTRICT"))
    medico_id: Mapped[int] = mapped_column(ForeignKey("doctors.id", ondelete="RESTRICT"))
    especialidad_id: Mapped[int] = mapped_column(ForeignKey("specialties.id", ondelete="RESTRICT"))
    fecha: Mapped[str] = mapped_column(String(25))   # ISO datetime "YYYY-MM-DDTHH:MM"
    duracion_min: Mapped[int] = mapped_column(Integer, default=30)
    estado: Mapped[TurnoEstado] = mapped_column(Enum(TurnoEstado), default=TurnoEstado.Reservado)
    receta_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # opcional: relaciones (no requeridas por endpoints)
    paciente = relationship("Patient")
    medico = relationship("Doctor")
    especialidad = relationship("Specialty")
