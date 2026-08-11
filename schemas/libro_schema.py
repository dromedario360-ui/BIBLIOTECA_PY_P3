from pydantic import BaseModel
from typing import Optional


class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: Optional[str] = None
    stock: int = 1


class LibroCrear(LibroBase):
    pass


class LibroActualizar(LibroBase):
    pass


class LibroRespuesta(LibroBase):
    id: int
    disponible: bool

    class Config:
        from_attributes = True
