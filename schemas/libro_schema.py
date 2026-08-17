from pydantic import BaseModel
from typing import Optional


class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: Optional[str] = None
    stock: int = 1
    precio: float = 0


class LibroCrear(LibroBase):
    pass


class LibroActualizar(LibroBase):
    pass


class LibroRespuesta(LibroBase):
    id: int
    disponible: bool
    imagen: Optional[str] = None

    class Config:
        from_attributes = True
