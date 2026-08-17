from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
import os, uuid
from models.libro import Libro
from schemas.libro_schema import LibroCrear, LibroActualizar, LibroRespuesta
from services.libro_service import LibroService
from repositories.libro_repository_sqlalchemy import LibroRepositorySQLAlchemy

router = APIRouter(prefix="/libros", tags=["Libros"])
service = LibroService(LibroRepositorySQLAlchemy())

CARPETA_IMAGENES = "web/static/uploads/libros"


@router.get("/", response_model=List[LibroRespuesta])
def listar_libros(q: Optional[str] = None):
    if q:
        return service.buscar(q)
    return service.listar()


@router.get("/{libro_id}", response_model=LibroRespuesta)
def obtener_libro(libro_id: int):
    libro = service.obtener(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.post("/", response_model=LibroRespuesta, status_code=201)
def crear_libro(datos: LibroCrear):
    libro = Libro(**datos.model_dump(), disponible=datos.stock > 0)
    return service.crear(libro)


@router.put("/{libro_id}", response_model=LibroRespuesta)
def actualizar_libro(libro_id: int, datos: LibroActualizar):
    libro = Libro(id=libro_id, **datos.model_dump(), disponible=datos.stock > 0)
    actualizado = service.actualizar(libro)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return actualizado


@router.post("/{libro_id}/imagen", response_model=LibroRespuesta)
def subir_imagen_libro(libro_id: int, archivo: UploadFile = File(...)):
    if not service.obtener(libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    extension = os.path.splitext(archivo.filename)[1]
    nombre_archivo = f"libro_{libro_id}_{uuid.uuid4().hex[:8]}{extension}"
    ruta_completa = os.path.join(CARPETA_IMAGENES, nombre_archivo)
    os.makedirs(CARPETA_IMAGENES, exist_ok=True)
    with open(ruta_completa, "wb") as f:
        f.write(archivo.file.read())
    ruta_publica = f"/static/uploads/libros/{nombre_archivo}"
    return service.actualizar_imagen(libro_id, ruta_publica)


@router.delete("/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int):
    if not service.eliminar(libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
