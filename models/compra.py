from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database.conexion import Base


class Compra(Base):
    __tablename__ = "compras"
    id = Column(Integer, primary_key=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    precio = Column(Float, nullable=False, default=0)
    fecha_compra = Column(DateTime, default=datetime.now)

    libro = relationship("Libro")
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"<Compra #{self.id} - libro={self.libro_id}>"
