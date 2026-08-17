from fastapi import APIRouter, HTTPException
from typing import List
from models.compra import Compra
from schemas.compra_schema import CompraCrear, CompraRespuesta
from repositories.compra_repository_sqlalchemy import CompraRepositorySQLAlchemy
from repositories.libro_repository_sqlalchemy import LibroRepositorySQLAlchemy

router = APIRouter(prefix="/compras", tags=["Compras"])
compra_repo = CompraRepositorySQLAlchemy()
libro_repo = LibroRepositorySQLAlchemy()


@router.get("/", response_model=List[CompraRespuesta])
def listar_compras():
    return compra_repo.obtener_todas()


@router.get("/usuario/{usuario_id}", response_model=List[CompraRespuesta])
def listar_compras_por_usuario(usuario_id: int):
    return compra_repo.obtener_por_usuario(usuario_id)


@router.post("/", response_model=CompraRespuesta, status_code=201)
def registrar_compra(datos: CompraCrear):
    libro = libro_repo.obtener_por_id(datos.libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    compra = Compra(libro_id=datos.libro_id, usuario_id=datos.usuario_id, precio=libro.precio)
    return compra_repo.crear(compra)
