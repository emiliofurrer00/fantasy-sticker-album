from fastapi import APIRouter, Depends, HTTPException, status

from app import crud, models
from app.dependencies import DbSession, CurrentUser, get_current_user_from_session
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

    sticker = crud.create_sticker(db, sticker_data, current_user.id)
    return sticker