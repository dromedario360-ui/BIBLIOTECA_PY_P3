from pydantic import BaseModel
from datetime import datetime


class CompraCrear(BaseModel):
    libro_id: int
    usuario_id: int


class CompraRespuesta(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    precio: float
    fecha_compra: datetime

    class Config:
        from_attributes = True
