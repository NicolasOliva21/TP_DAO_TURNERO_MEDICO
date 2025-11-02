from pydantic import BaseModel, EmailStr
from typing import Optional

class DoctorBase(BaseModel):
    nombre: str
    apellido: str
    dni: str
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    matricula: str

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    id: int
    activo: bool
