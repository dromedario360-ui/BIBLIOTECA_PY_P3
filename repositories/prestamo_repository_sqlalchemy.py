from typing import List, Optional
from datetime import datetime
from database.conexion import SessionLocal
from models.prestamo import Prestamo
from repositories.prestamo_repository import IPrestamoRepository


class PrestamoRepositorySQLAlchemy(IPrestamoRepository):
    def obtener_todos(self) -> List[Prestamo]:
        with SessionLocal() as db:
            return db.query(Prestamo).all()

    def obtener_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        with SessionLocal() as db:
            return db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()

    def obtener_activos_por_libro(self, libro_id: int) -> List[Prestamo]:
        with SessionLocal() as db:
            return db.query(Prestamo).filter(
                Prestamo.libro_id == libro_id, Prestamo.devuelto == False
            ).all()

    def crear(self, prestamo: Prestamo) -> Prestamo:
        with SessionLocal() as db:
            db.add(prestamo)
            db.commit()
            db.refresh(prestamo)
            return prestamo

    def marcar_devuelto(self, prestamo_id: int) -> Optional[Prestamo]:
        with SessionLocal() as db:
            prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
            if not prestamo:
                return None
            prestamo.devuelto = True
            prestamo.fecha_devolucion = datetime.now()
            db.commit()
            db.refresh(prestamo)
            return prestamo
