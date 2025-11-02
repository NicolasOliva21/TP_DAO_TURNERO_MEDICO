from pydantic import BaseModel
from typing import Optional

class SpecialtyBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyUpdate(SpecialtyBase):
    pass

class SpecialtyOut(SpecialtyBase):
    id: int
    activa: bool
