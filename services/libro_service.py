from typing import List, Optional
from models.libro import Libro
from repositories.libro_repository import ILibroRepository


class LibroService:
    def __init__(self, repositorio: ILibroRepository):
        self.repositorio = repositorio

    def listar(self) -> List[Libro]:
        return self.repositorio.obtener_todos()

    def obtener(self, libro_id: int) -> Optional[Libro]:
        return self.repositorio.obtener_por_id(libro_id)

    def buscar(self, texto: str) -> List[Libro]:
        return self.repositorio.buscar(texto)

    def crear(self, libro: Libro) -> Libro:
        return self.repositorio.crear(libro)

    def actualizar(self, libro: Libro) -> Optional[Libro]:
        return self.repositorio.actualizar(libro)

    def eliminar(self, libro_id: int) -> bool:
        return self.repositorio.eliminar(libro_id)
