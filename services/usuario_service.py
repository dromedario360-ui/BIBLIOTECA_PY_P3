from typing import List, Optional
from models.usuario import Usuario
from repositories.usuario_repository import IUsuarioRepository


class UsuarioService:
    def __init__(self, repositorio: IUsuarioRepository):
        self.repositorio = repositorio

    def listar(self) -> List[Usuario]:
        return self.repositorio.obtener_todos()

    def obtener(self, usuario_id: int) -> Optional[Usuario]:
        return self.repositorio.obtener_por_id(usuario_id)

    def crear(self, usuario: Usuario) -> Usuario:
        return self.repositorio.crear(usuario)

    def actualizar(self, usuario: Usuario) -> Optional[Usuario]:
        return self.repositorio.actualizar(usuario)

    def actualizar_foto(self, usuario_id: int, ruta_foto: str) -> Optional[Usuario]:
        return self.repositorio.actualizar_foto(usuario_id, ruta_foto)

    def eliminar(self, usuario_id: int) -> bool:
        return self.repositorio.eliminar(usuario_id)
