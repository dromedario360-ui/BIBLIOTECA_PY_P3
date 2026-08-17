from typing import List
from database.conexion import SessionLocal
from models.compra import Compra
from repositories.compra_repository import ICompraRepository


class CompraRepositorySQLAlchemy(ICompraRepository):
    def obtener_todas(self) -> List[Compra]:
        with SessionLocal() as db:
            return db.query(Compra).all()

    def obtener_por_usuario(self, usuario_id: int) -> List[Compra]:
        with SessionLocal() as db:
            return db.query(Compra).filter(Compra.usuario_id == usuario_id).all()

    def crear(self, compra: Compra) -> Compra:
        with SessionLocal() as db:
            db.add(compra)
            db.commit()
            db.refresh(compra)
            return compra
