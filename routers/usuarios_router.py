from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import os, uuid
from models.usuario import Usuario
from schemas.usuario_schema import UsuarioCrear, UsuarioActualizar, UsuarioRespuesta
from services.usuario_service import UsuarioService
from repositories.usuario_repository_sqlalchemy import UsuarioRepositorySQLAlchemy

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
service = UsuarioService(UsuarioRepositorySQLAlchemy())

CARPETA_FOTOS = "web/static/uploads/usuarios"


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


@router.post("/{usuario_id}/foto", response_model=UsuarioRespuesta)
def subir_foto_usuario(usuario_id: int, archivo: UploadFile = File(...)):
    if not service.obtener(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    extension = os.path.splitext(archivo.filename)[1]
    nombre_archivo = f"usuario_{usuario_id}_{uuid.uuid4().hex[:8]}{extension}"
    ruta_completa = os.path.join(CARPETA_FOTOS, nombre_archivo)
    os.makedirs(CARPETA_FOTOS, exist_ok=True)
    with open(ruta_completa, "wb") as f:
        f.write(archivo.file.read())
    ruta_publica = f"/static/uploads/usuarios/{nombre_archivo}"
    return service.actualizar_foto(usuario_id, ruta_publica)


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: int):
    if not service.eliminar(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
