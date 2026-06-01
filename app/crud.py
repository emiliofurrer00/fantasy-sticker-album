from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.schemas import StickerCreate


def get_user_by_username(db: Session, username: str) -> models.User | None:
    statement = select(models.User).where(models.User.username == username)
    return db.scalar(statement)


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    statement = select(models.User).where(models.User.id == user_id)
    return db.scalar(statement)


def get_stickers_by_owner(db: Session, owner_id: int) -> list[models.Sticker]:
    statement = select(models.Sticker).where(models.Sticker.owner_id == owner_id)
    return list(db.scalars(statement))

def get_sticker_by_owner_name_and_collection(
    db: Session,
    owner_id: int,
    name: str,
    collection_name: str | None = None,
) -> models.Sticker | None:
    statement = select(models.Sticker).where(
        models.Sticker.owner_id == owner_id,
        models.Sticker.name == name,
        models.Sticker.collection_name == collection_name,
    )
    return db.scalar(statement)

def create_sticker(
        db: Session,
        sticker_data: StickerCreate,
        owner_id: int
) -> models.Sticker:
    new_sticker = models.Sticker(
        name=sticker_data.name,
        collection_name=sticker_data.collection_name,
        role=sticker_data.role,
        number=sticker_data.number,
        image_url=sticker_data.image_url,
        owner_id=owner_id,
        is_favorite=sticker_data.is_favorite or False
    )

    db.add(new_sticker)
    db.commit()
    db.refresh(new_sticker)

    return new_sticker