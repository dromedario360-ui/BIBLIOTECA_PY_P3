from typing import List, Optional
from sqlalchemy import or_
from database.conexion import SessionLocal
from models.libro import Libro
from repositories.libro_repository import ILibroRepository


class LibroRepositorySQLAlchemy(ILibroRepository):
    def obtener_todos(self) -> List[Libro]:
        with SessionLocal() as db:
            return db.query(Libro).all()

    def obtener_por_id(self, libro_id: int) -> Optional[Libro]:
        with SessionLocal() as db:
            return db.query(Libro).filter(Libro.id == libro_id).first()

    def buscar(self, texto: str) -> List[Libro]:
        with SessionLocal() as db:
            patron = f"%{texto}%"
            return db.query(Libro).filter(
                or_(Libro.titulo.ilike(patron), Libro.autor.ilike(patron), Libro.categoria.ilike(patron))
            ).all()

    def crear(self, libro: Libro) -> Libro:
        with SessionLocal() as db:
            db.add(libro)
            db.commit()
            db.refresh(libro)
            return libro

    def actualizar(self, libro: Libro) -> Libro:
        with SessionLocal() as db:
            existente = db.query(Libro).filter(Libro.id == libro.id).first()
            if not existente:
                return None
            existente.titulo = libro.titulo
            existente.autor = libro.autor
            existente.isbn = libro.isbn
            existente.categoria = libro.categoria
            existente.stock = libro.stock
            existente.disponible = libro.disponible
            db.commit()
            db.refresh(existente)
            return existente

    def eliminar(self, libro_id: int) -> bool:
        with SessionLocal() as db:
            libro = db.query(Libro).filter(Libro.id == libro_id).first()
            if not libro:
                return False
            db.delete(libro)
            db.commit()
            return True
