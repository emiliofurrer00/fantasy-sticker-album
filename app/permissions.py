from app import models


def can_view_album(user: models.User | None, album: models.Album) -> bool:
    return album.is_public or (user is not None and album.owner_id == user.id)
