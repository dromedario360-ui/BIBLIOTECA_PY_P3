from abc import ABC, abstractmethod
from typing import List
from models.compra import Compra


class ICompraRepository(ABC):
    @abstractmethod
    def obtener_todas(self) -> List[Compra]:
        pass

    @abstractmethod
    def obtener_por_usuario(self, usuario_id: int) -> List[Compra]:
        pass

    @abstractmethod
    def crear(self, compra: Compra) -> Compra:
        pass
