from abc import ABC, abstractmethod
from typing import List, Optional
from models.libro import Libro


class ILibroRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[Libro]:
        pass

    @abstractmethod
    def obtener_por_id(self, libro_id: int) -> Optional[Libro]:
        pass

    @abstractmethod
    def buscar(self, texto: str) -> List[Libro]:
        pass

    @abstractmethod
    def crear(self, libro: Libro) -> Libro:
        pass

    @abstractmethod
    def actualizar(self, libro: Libro) -> Libro:
        pass

    @abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        pass
