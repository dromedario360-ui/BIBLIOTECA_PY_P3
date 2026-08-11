from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PrestamoCrear(BaseModel):
    libro_id: int
    usuario_id: int


class PrestamoRespuesta(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None
    devuelto: bool

    class Config:
        from_attributes = True
