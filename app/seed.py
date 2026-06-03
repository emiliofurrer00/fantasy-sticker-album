from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password
from app.crud import get_user_by_username


def seed_data(db: Session) -> None:
    try:
        demouser = get_user_by_username(db, "demouser")
        if demouser is None:
            demouser = models.User(
                username="demouser",
                password_hash=hash_password("demouser123"),
            )
            db.add(demouser)
            db.flush()

        demo_album = db.scalar(
            select(models.Album).where(
                models.Album.owner_id == demouser.id,
                models.Album.title == "Mundial 2026",
            )
        )
        if demo_album is not None:
            db.commit()
            return

        public_album = models.Album(
            title="Mundial 2026",
            description="Album publico de ejemplo.",
            is_public=True,
            owner_id=demouser.id,
        )
        private_album = models.Album(
            title="Favoritas Argentina",
            description="Album privado de ejemplo.",
            is_public=False,
            owner_id=demouser.id,
        )
        db.add_all([public_album, private_album])
        db.flush()

        db.add_all(
            [
                models.Sticker(
                    name="Lionel Messi",
                    collection_name="Argentina 2026",
                    role="Delantero",
                    number=10,
                    image_url="https://example.com/messi.png",
                    is_favorite=True,
                    owner_id=demouser.id,
                    album_id=private_album.id,
                ),
                models.Sticker(
                    name="Dibu Martinez",
                    collection_name="Argentina 2026",
                    role="Arquero",
                    number=23,
                    image_url="https://example.com/dibu.png",
                    is_favorite=True,
                    owner_id=demouser.id,
                    album_id=public_album.id,
                ),
                models.Sticker(
                    name="Enzo Fernandez",
                    collection_name="Argentina 2026",
                    role="Mediocampista",
                    number=24,
                    image_url="https://example.com/enzo.png",
                    owner_id=demouser.id,
                ),
            ]
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
