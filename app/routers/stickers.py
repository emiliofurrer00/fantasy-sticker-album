from fastapi import APIRouter, HTTPException, status

from app import crud
from app.dependencies import CurrentUser, DbSession
from app.schemas import StickerCreate, StickerRead

router = APIRouter(prefix="/api/stickers", tags=["stickers"])


@router.get("/", response_model=list[StickerRead])
def read_stickers(
    current_user: CurrentUser,
    db: DbSession,
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    stickers = crud.get_stickers_by_owner(db, current_user.id)
    return stickers


@router.post("/", response_model=StickerRead, status_code=status.HTTP_201_CREATED)
def create_sticker(
    sticker_data: StickerCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    if sticker_data.album_id is not None:
        album = crud.get_album_by_id(db, sticker_data.album_id)
        if album is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found",
            )

        if album.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot add sticker to an album you do not own",
            )

    sticker = crud.create_sticker(db, sticker_data, current_user.id)
    return sticker
