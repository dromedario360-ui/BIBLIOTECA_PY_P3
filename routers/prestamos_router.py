from fastapi import APIRouter, HTTPException
from typing import List
from schemas.prestamo_schema import PrestamoCrear, PrestamoRespuesta
from services.prestamo_service import PrestamoService, StockNoDisponibleError, LibroNoEncontradoError
from repositories.prestamo_repository_sqlalchemy import PrestamoRepositorySQLAlchemy
from repositories.libro_repository_sqlalchemy import LibroRepositorySQLAlchemy

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])
service = PrestamoService(PrestamoRepositorySQLAlchemy(), LibroRepositorySQLAlchemy())


@router.get("/", response_model=List[PrestamoRespuesta])
def listar_prestamos():
    return service.listar()


@router.post("/", response_model=PrestamoRespuesta, status_code=201)
def crear_prestamo(datos: PrestamoCrear):
    try:
        return service.prestar(datos.libro_id, datos.usuario_id)
    except LibroNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StockNoDisponibleError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{prestamo_id}/devolver", response_model=PrestamoRespuesta)
def devolver_prestamo(prestamo_id: int):
    prestamo = service.devolver(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return prestamo
