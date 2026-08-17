from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="web/templates")

USUARIO_VALIDO = "bibliotecario"
PASSWORD_VALIDO = "biblioteca123"


@router.get("/login", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login", response_class=HTMLResponse)
def procesar_login(request: Request, usuario: str = Form(...), password: str = Form(...)):
    if usuario.strip() == USUARIO_VALIDO and password.strip() == PASSWORD_VALIDO:
        respuesta = RedirectResponse(url="/panel", status_code=status.HTTP_302_FOUND)
        respuesta.set_cookie(key="sesion_biblioteca", value="autenticado", httponly=True, max_age=3600)
        return respuesta
    return templates.TemplateResponse(
        request, "login.html", {"error": "Usuario o contrasena incorrectos"}
    )


@router.get("/panel", response_class=HTMLResponse)
def mostrar_panel(request: Request):
    if request.cookies.get("sesion_biblioteca") != "autenticado":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request, "panel.html", {})


@router.get("/logout")
def logout():
    respuesta = RedirectResponse(url="/login")
    respuesta.delete_cookie("sesion_biblioteca")
    return respuesta
