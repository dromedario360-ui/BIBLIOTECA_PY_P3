from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.libro import Libro
from schemas.libro_schema import LibroCrear, LibroActualizar, LibroRespuesta
from services.libro_service import LibroService
from repositories.libro_repository_sqlalchemy import LibroRepositorySQLAlchemy

router = APIRouter(prefix="/libros", tags=["Libros"])
service = LibroService(LibroRepositorySQLAlchemy())


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


@router.delete("/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int):
    if not service.eliminar(libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
