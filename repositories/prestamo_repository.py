from abc import ABC, abstractmethod
from typing import List, Optional
from models.prestamo import Prestamo


class IPrestamoRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[Prestamo]:
        pass

    @abstractmethod
    def obtener_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        pass

    @abstractmethod
    def obtener_activos_por_libro(self, libro_id: int) -> List[Prestamo]:
        pass

    @abstractmethod
    def crear(self, prestamo: Prestamo) -> Prestamo:
        pass

    @abstractmethod
    def marcar_devuelto(self, prestamo_id: int) -> Optional[Prestamo]:
        pass
