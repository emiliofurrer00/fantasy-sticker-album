from sqlalchemy.orm import Session

from app import models


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_stickers_by_owner(db: Session, owner_id: int) -> list[models.Sticker]:
    return (
        db.query(models.Sticker)
        .filter(models.Sticker.owner_id == owner_id)
        .all()
    )