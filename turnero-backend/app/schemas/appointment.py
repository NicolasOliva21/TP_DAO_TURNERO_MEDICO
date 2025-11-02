from pydantic import BaseModel, field_validator
from typing import Optional, Literal

TurnoEstado = Literal["Reservado", "Cancelado", "Reprogramado", "Atendido"]

class AppointmentBase(BaseModel):
    paciente_id: int
    medico_id: int
    especialidad_id: int
    fecha: str               # "YYYY-MM-DDTHH:MM"
    duracion_min: int = 30
    receta_url: Optional[str] = None

    @field_validator("fecha")
    @classmethod
    def valid_dt(cls, v: str):
        assert "T" in v and len(v) >= 16, "fecha debe ser ISO 'YYYY-MM-DDTHH:MM'"
        return v

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    fecha: Optional[str] = None
    duracion_min: Optional[int] = None
    estado: Optional[TurnoEstado] = None
    receta_url: Optional[str] = None

class AppointmentOut(AppointmentBase):
    id: int
    estado: TurnoEstado
