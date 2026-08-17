from fastapi import APIRouter, Request, Form, status, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os, uuid
from repositories.libro_repository_sqlalchemy import LibroRepositorySQLAlchemy
from repositories.usuario_repository_sqlalchemy import UsuarioRepositorySQLAlchemy
from repositories.prestamo_repository_sqlalchemy import PrestamoRepositorySQLAlchemy
from repositories.compra_repository_sqlalchemy import CompraRepositorySQLAlchemy
from models.compra import Compra

router = APIRouter(tags=["Cliente"])
templates = Jinja2Templates(directory="web/templates")

libro_repo = LibroRepositorySQLAlchemy()
usuario_repo = UsuarioRepositorySQLAlchemy()
prestamo_repo = PrestamoRepositorySQLAlchemy()
compra_repo = CompraRepositorySQLAlchemy()

CARPETA_FOTOS = "web/static/uploads/usuarios"


@router.get("/catalogo", response_class=HTMLResponse)
def ver_catalogo(request: Request, q: str = None):
    libros = libro_repo.buscar(q) if q else libro_repo.obtener_todos()
    socio_id = request.cookies.get("sesion_socio")
    return templates.TemplateResponse(request, "catalogo.html", {"libros": libros, "q": q or "", "sesion_activa": bool(socio_id)})


@router.get("/socio/login", response_class=HTMLResponse)
def mostrar_login_socio(request: Request):
    return templates.TemplateResponse(request, "socio_login.html", {"error": None})


@router.post("/socio/login", response_class=HTMLResponse)
def procesar_login_socio(request: Request, correo: str = Form(...)):
    socios = usuario_repo.obtener_todos()
    socio = next((s for s in socios if s.correo.lower() == correo.strip().lower()), None)
    if not socio:
        return templates.TemplateResponse(
            request, "socio_login.html", {"error": "No encontramos ese correo registrado. Pide al bibliotecario que te registre primero."}
        )
    respuesta = RedirectResponse(url="/socio/panel", status_code=status.HTTP_302_FOUND)
    respuesta.set_cookie(key="sesion_socio", value=str(socio.id), httponly=True, max_age=3600)
    return respuesta


def _obtener_socio_actual(request: Request):
    socio_id = request.cookies.get("sesion_socio")
    if not socio_id:
        return None
    return usuario_repo.obtener_por_id(int(socio_id))


@router.get("/socio/panel", response_class=HTMLResponse)
def panel_socio(request: Request):
    socio = _obtener_socio_actual(request)
    if not socio:
        return RedirectResponse(url="/socio/login")

    todos_prestamos = prestamo_repo.obtener_todos()
    mis_prestamos = [p for p in todos_prestamos if p.usuario_id == socio.id]
    mis_prestamos.sort(key=lambda p: p.fecha_prestamo, reverse=True)
    prestamos_con_libro = []
    for p in mis_prestamos:
        libro = libro_repo.obtener_por_id(p.libro_id)
        prestamos_con_libro.append({"prestamo": p, "libro": libro})

    mis_compras = compra_repo.obtener_por_usuario(socio.id)
    mis_compras.sort(key=lambda c: c.fecha_compra, reverse=True)
    compras_con_libro = []
    for c in mis_compras:
        libro = libro_repo.obtener_por_id(c.libro_id)
        compras_con_libro.append({"compra": c, "libro": libro})

    return templates.TemplateResponse(
        request, "socio_panel.html",
        {"socio": socio, "prestamos": prestamos_con_libro, "compras": compras_con_libro}
    )


@router.post("/socio/foto")
def subir_foto_socio(request: Request, archivo: UploadFile = File(...)):
    socio = _obtener_socio_actual(request)
    if not socio:
        raise HTTPException(status_code=401, detail="Debes iniciar sesion")
    extension = os.path.splitext(archivo.filename)[1]
    nombre_archivo = f"usuario_{socio.id}_{uuid.uuid4().hex[:8]}{extension}"
    os.makedirs(CARPETA_FOTOS, exist_ok=True)
    ruta_completa = os.path.join(CARPETA_FOTOS, nombre_archivo)
    with open(ruta_completa, "wb") as f:
        f.write(archivo.file.read())
    usuario_repo.actualizar_foto(socio.id, f"/static/uploads/usuarios/{nombre_archivo}")
    return RedirectResponse(url="/socio/panel", status_code=status.HTTP_302_FOUND)


@router.post("/socio/comprar/{libro_id}")
def comprar_libro(request: Request, libro_id: int):
    socio = _obtener_socio_actual(request)
    if not socio:
        return RedirectResponse(url="/socio/login")
    libro = libro_repo.obtener_por_id(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    compra = Compra(libro_id=libro_id, usuario_id=socio.id, precio=libro.precio)
    compra_repo.crear(compra)
    return RedirectResponse(url="/socio/panel", status_code=status.HTTP_302_FOUND)


@router.get("/socio/logout")
def logout_socio():
    respuesta = RedirectResponse(url="/socio/login")
    respuesta.delete_cookie("sesion_socio")
    return respuesta
