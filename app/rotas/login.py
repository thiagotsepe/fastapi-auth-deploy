from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated

from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.modelos.usuario import Usuario
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio, UsuarioCriarAtualizar
from app.dependencias import UsuarioRepositorio, obter_usuario_repositorio

router = APIRouter(
    prefix="/login"
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def pagina_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/")
async def login(request: Request, usuario_repositorio: Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)], email: str = Form(...), senha: str = Form(...)):
    usuario = await usuario_repositorio.buscar_usuario_por_email_senha(email, senha)
    if usuario:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)
        return response
    
    return templates.TemplateResponse(request=request, name="login.html", context={
        "email": email,
        "senha": senha,
        "error": "Credenciais inválidas"
    })