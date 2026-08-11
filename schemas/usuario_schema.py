from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: Optional[str] = None


class UsuarioCrear(UsuarioBase):
    pass


class UsuarioActualizar(UsuarioBase):
    pass


class UsuarioRespuesta(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
