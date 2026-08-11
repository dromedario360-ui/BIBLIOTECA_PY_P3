from fastapi import FastAPI
from database.conexion import crear_base_datos
from routers import libros_router, usuarios_router, prestamos_router

app = FastAPI(
    title="Sistema de Gestion de Biblioteca",
    description="API REST para el Proyecto Final de Programacion III",
    version="1.0.0",
)

crear_base_datos()

app.include_router(libros_router.router)
app.include_router(usuarios_router.router)
app.include_router(prestamos_router.router)


@app.get("/")
def raiz():
    return {"mensaje": "API de Biblioteca funcionando. Visita /docs para probarla."}
