from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.conexion import Base


class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_prestamo = Column(DateTime, default=datetime.now)
    fecha_devolucion = Column(DateTime, nullable=True)
    devuelto = Column(Boolean, nullable=False, default=False)

    libro = relationship("Libro")
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"<Prestamo #{self.id} - devuelto={self.devuelto}>"
