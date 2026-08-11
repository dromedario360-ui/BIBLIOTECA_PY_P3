from fastapi import APIRouter, HTTPException
from typing import List
from models.usuario import Usuario
from schemas.usuario_schema import UsuarioCrear, UsuarioActualizar, UsuarioRespuesta
from services.usuario_service import UsuarioService
from repositories.usuario_repository_sqlalchemy import UsuarioRepositorySQLAlchemy

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
service = UsuarioService(UsuarioRepositorySQLAlchemy())


@router.get("/", response_model=List[UsuarioRespuesta])
def listar_usuarios():
    return service.listar()


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def obtener_usuario(usuario_id: int):
    usuario = service.obtener(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioRespuesta, status_code=201)
def crear_usuario(datos: UsuarioCrear):
    usuario = Usuario(**datos.model_dump())
    return service.crear(usuario)


@router.put("/{usuario_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(usuario_id: int, datos: UsuarioActualizar):
    usuario = Usuario(id=usuario_id, **datos.model_dump())
    actualizado = service.actualizar(usuario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int):
    if not service.eliminar(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
