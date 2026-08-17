import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

RAIZ_PROYECTO = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(RAIZ_PROYECTO, "..", "biblioteca.db")

engine = create_engine("sqlite:///" + RUTA_BD, echo=False)
SessionLocal = sessionmaker(bind=engine)


def crear_base_datos():
    from models.libro import Libro
    from models.usuario import Usuario
    from models.prestamo import Prestamo
    from models.compra import Compra
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
