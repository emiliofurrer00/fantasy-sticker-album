from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.auth import authenticate_user
from app.dependencies import CurrentUser, DbSession

router = APIRouter()
templates = Jinja2Templates(directory="app/templates/pages")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, current_user: CurrentUser):
    if current_user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(request, "login.html")


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    db: DbSession,
    username: str = Form(...),
    password: str = Form(...),
):
    user = authenticate_user(db, username, password)
    if user is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid username or password"},
        )

    request.session["user_id"] = user.id
    response = RedirectResponse("/", status_code=302)

    return response


@router.get("/", response_class=HTMLResponse)
def root(
    request: Request,
    current_user: CurrentUser,
    db: DbSession,
):
    if current_user is None:
        return RedirectResponse("/login", status_code=302)

    stickers = crud.get_stickers_by_owner(db, current_user.id)
    albums = crud.get_albums_by_owner(db, current_user.id)
    public_albums = crud.get_public_albums(db)

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "user": current_user,
            "stickers": stickers,
            "albums": albums,
            "public_albums": public_albums,
        },
    )


@router.post("/logout")
def logout(
    request: Request,
):
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    request.session.clear()
    return response
