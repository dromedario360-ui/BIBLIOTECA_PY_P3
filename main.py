from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database.conexion import crear_base_datos
from routers import libros_router, usuarios_router, prestamos_router, web_router, cliente_router, compras_router

app = FastAPI(
    title="Sistema de Gestion de Biblioteca",
    description="API REST para el Proyecto Final de Programacion III",
    version="1.0.0",
)

crear_base_datos()

app.mount("/static", StaticFiles(directory="web/static"), name="static")

app.include_router(libros_router.router)
app.include_router(usuarios_router.router)
app.include_router(prestamos_router.router)
app.include_router(web_router.router)
app.include_router(cliente_router.router)
app.include_router(compras_router.router)


@app.get("/")
def raiz():
    return RedirectResponse(url="/catalogo")
