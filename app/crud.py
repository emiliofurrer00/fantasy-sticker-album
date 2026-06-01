from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models


def get_user_by_username(db: Session, username: str) -> models.User | None:
    statement = select(models.User).where(models.User.username == username)
    return db.scalar(statement)


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    statement = select(models.User).where(models.User.id == user_id)
    return db.scalar(statement)


def get_stickers_by_owner(db: Session, owner_id: int) -> list[models.Sticker]:
    statement = select(models.Sticker).where(models.Sticker.owner_id == owner_id)
    return list(db.scalars(statement))