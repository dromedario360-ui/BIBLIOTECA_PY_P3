from sqlalchemy import Column, Integer, String
from database.conexion import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    telefono = Column(String, nullable=True)

    def __repr__(self):
        return f"<Usuario: {self.nombre}>"
