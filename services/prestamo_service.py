from typing import List
from models.prestamo import Prestamo
from repositories.prestamo_repository import IPrestamoRepository
from repositories.libro_repository import ILibroRepository


class StockNoDisponibleError(Exception):
    pass


class LibroNoEncontradoError(Exception):
    pass


class PrestamoService:
    """Contiene las reglas de negocio: no se puede prestar un libro
    sin stock disponible, y al devolverlo el stock vuelve a subir."""

    def __init__(self, prestamo_repo: IPrestamoRepository, libro_repo: ILibroRepository):
        self.prestamo_repo = prestamo_repo
        self.libro_repo = libro_repo

    def listar(self) -> List[Prestamo]:
        return self.prestamo_repo.obtener_todos()

    def prestar(self, libro_id: int, usuario_id: int) -> Prestamo:
        libro = self.libro_repo.obtener_por_id(libro_id)
        if not libro:
            raise LibroNoEncontradoError(f"Libro {libro_id} no existe")
        if libro.stock <= 0:
            raise StockNoDisponibleError(f"No hay stock disponible de '{libro.titulo}'")

        libro.stock -= 1
        libro.disponible = libro.stock > 0
        self.libro_repo.actualizar(libro)

        prestamo = Prestamo(libro_id=libro_id, usuario_id=usuario_id)
        return self.prestamo_repo.crear(prestamo)

    def devolver(self, prestamo_id: int) -> Prestamo:
        prestamo = self.prestamo_repo.marcar_devuelto(prestamo_id)
        if prestamo:
            libro = self.libro_repo.obtener_por_id(prestamo.libro_id)
            if libro:
                libro.stock += 1
                libro.disponible = True
                self.libro_repo.actualizar(libro)
        return prestamo
