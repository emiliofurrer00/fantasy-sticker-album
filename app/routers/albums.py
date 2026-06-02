from fastapi import APIRouter, HTTPException, status

from app import crud
from app.dependencies import CurrentUser, DbSession
from app.permissions import can_view_album
from app.schemas import AlbumCreate, AlbumRead

router = APIRouter(prefix="/api/albums", tags=["albums"])

#TO DO: add page for public albums, and for my albums
@router.get("/public", response_model=list[AlbumRead])
def read_public_albums(db: DbSession):
    return crud.get_public_albums(db)


@router.get("/me", response_model=list[AlbumRead])
def read_my_albums(
    current_user: CurrentUser,
    db: DbSession,
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return crud.get_albums_by_owner(db, current_user.id)


@router.get("/{album_id}", response_model=AlbumRead)
def read_album(
    album_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    album = crud.get_album_by_id(db, album_id)
    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found",
        )

    if not can_view_album(current_user, album):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Album is private",
        )

    return album


@router.post("/", response_model=AlbumRead, status_code=status.HTTP_201_CREATED)
def create_album(
    album_data: AlbumCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return crud.create_album(db, album_data, current_user.id)
