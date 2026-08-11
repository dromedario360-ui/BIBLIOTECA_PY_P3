from typing import List, Optional
from database.conexion import SessionLocal
from models.usuario import Usuario
from repositories.usuario_repository import IUsuarioRepository


class UsuarioRepositorySQLAlchemy(IUsuarioRepository):
    def obtener_todos(self) -> List[Usuario]:
        with SessionLocal() as db:
            return db.query(Usuario).all()

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        with SessionLocal() as db:
            return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def crear(self, usuario: Usuario) -> Usuario:
        with SessionLocal() as db:
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            return usuario

    def actualizar(self, usuario: Usuario) -> Usuario:
        with SessionLocal() as db:
            existente = db.query(Usuario).filter(Usuario.id == usuario.id).first()
            if not existente:
                return None
            existente.nombre = usuario.nombre
            existente.correo = usuario.correo
            existente.telefono = usuario.telefono
            db.commit()
            db.refresh(existente)
            return existente

    def eliminar(self, usuario_id: int) -> bool:
        with SessionLocal() as db:
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                return False
            db.delete(usuario)
            db.commit()
            return True
