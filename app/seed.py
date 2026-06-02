from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password
from app.crud import get_user_by_username


def seed_data(db: Session) -> None:
    if get_user_by_username(db, "demouser") is not None:
        return

    try:
        demouser = models.User(
            username="demouser",
            password_hash=hash_password("demouser123"),
        )
        db.add(demouser)
        db.commit()
        db.refresh(demouser)

        demo_stickers = [
            models.Sticker(
                name="Sticker 1",
                collection_name="Coleccion A",
                role="Jugador",
                number=1,
                image_url="https://example.com/sticker-1.png",
                owner_id=demouser.id,
            ),
            models.Sticker(
                name="Sticker 2",
                collection_name="Coleccion A",
                role="Portero",
                number=2,
                image_url="https://example.com/sticker-2.png",
                owner_id=demouser.id,
            ),
        ]
        db.add_all(demo_stickers)
        db.commit()
    except Exception:
        db.rollback()
        raise
