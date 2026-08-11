from abc import ABC, abstractmethod
from typing import List, Optional
from models.usuario import Usuario


class IUsuarioRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        pass

    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool:
        pass
