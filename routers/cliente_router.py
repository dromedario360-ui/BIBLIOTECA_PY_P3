from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repositories.libro_repository_sqlalchemy import LibroRepositorySQLAlchemy
from repositories.usuario_repository_sqlalchemy import UsuarioRepositorySQLAlchemy
from repositories.prestamo_repository_sqlalchemy import PrestamoRepositorySQLAlchemy

router = APIRouter(tags=["Cliente"])
templates = Jinja2Templates(directory="web/templates")

libro_repo = LibroRepositorySQLAlchemy()
usuario_repo = UsuarioRepositorySQLAlchemy()
prestamo_repo = PrestamoRepositorySQLAlchemy()


@router.get("/catalogo", response_class=HTMLResponse)
def ver_catalogo(request: Request, q: str = None):
    libros = libro_repo.buscar(q) if q else libro_repo.obtener_todos()
    return templates.TemplateResponse(request, "catalogo.html", {"libros": libros, "q": q or ""})


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


@router.get("/socio/panel", response_class=HTMLResponse)
def panel_socio(request: Request):
    socio_id = request.cookies.get("sesion_socio")
    if not socio_id:
        return RedirectResponse(url="/socio/login")
    socio = usuario_repo.obtener_por_id(int(socio_id))
    if not socio:
        return RedirectResponse(url="/socio/login")
    todos_prestamos = prestamo_repo.obtener_todos()
    mis_prestamos = [p for p in todos_prestamos if p.usuario_id == socio.id]
    prestamos_con_libro = []
    for p in mis_prestamos:
        libro = libro_repo.obtener_por_id(p.libro_id)
        prestamos_con_libro.append({"prestamo": p, "libro": libro})
    return templates.TemplateResponse(
        request, "socio_panel.html", {"socio": socio, "prestamos": prestamos_con_libro}
    )


@router.get("/socio/logout")
def logout_socio():
    respuesta = RedirectResponse(url="/socio/login")
    respuesta.delete_cookie("sesion_socio")
    return respuesta
