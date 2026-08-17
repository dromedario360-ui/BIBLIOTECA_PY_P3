from sqlalchemy import Column, Integer, String, Boolean
from database.conexion import Base

class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)
    categoria = Column(String, nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    disponible = Column(Boolean, nullable=False, default=True)
    imagen = Column(String, nullable=True)

    def __repr__(self):
        return f"<Libro: {self.titulo} ({self.autor})>"
