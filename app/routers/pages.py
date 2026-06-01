from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth import authenticate_user
from app.database import get_db
from app.dependencies import get_current_user_from_cookie
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, username, password)
    if user is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid username or password"},
        )
    
    response = RedirectResponse("/", status_code=302)
    
    response.set_cookie(key="user_id", value=str(user.id), httponly=True)
    return response

@router.get("/", response_class=HTMLResponse)
def root(
    request: Request,
    current_user: User | None = Depends(get_current_user_from_cookie),
):
    if current_user is None:
        return RedirectResponse("/login", status_code=302)
    
    return templates.TemplateResponse(request, "home.html", {"user": current_user})

@router.post("/logout")
def logout(
    response: Response,
):
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.delete_cookie("user_id")
    return response