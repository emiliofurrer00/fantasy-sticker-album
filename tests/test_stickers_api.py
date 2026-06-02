from app.auth import hash_password
from app.models import Album, User


def create_album_in_db(db_session, owner, *, is_public: bool = False) -> Album:
    album = Album(
        title="Album test",
        description="Album para tests de stickers",
        is_public=is_public,
        owner_id=owner.id,
    )
    db_session.add(album)
    db_session.commit()
    db_session.refresh(album)
    return album


def create_user_in_db(db_session, username: str) -> User:
    user = User(
        username=username,
        password_hash=hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_list_stickers_requires_authentication(client):
    response = client.get("/api/stickers/")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_list_stickers_returns_user_stickers(authenticated_client):
    response = authenticated_client.get("/api/stickers/")

    assert response.status_code == 200
    stickers = response.json()
    assert stickers == []


def test_create_sticker(authenticated_client):
    new_sticker_data = {
        "name": "Messi",
        "collection_name": "Argentina 2026",
        "role": "Delantero",
        "number": 10,
        "image_url": "http://example.com/messi.png",
        "is_favorite": True,
    }

    response = authenticated_client.post("/api/stickers/", json=new_sticker_data)

    assert response.status_code == 201
    created_sticker = response.json()
    assert created_sticker["name"] == new_sticker_data["name"]
    assert created_sticker["collection_name"] == new_sticker_data["collection_name"]
    assert created_sticker["role"] == new_sticker_data["role"]
    assert created_sticker["number"] == new_sticker_data["number"]
    assert created_sticker["image_url"] == new_sticker_data["image_url"]
    assert created_sticker["is_favorite"] == new_sticker_data["is_favorite"]
    assert "id" in created_sticker


def test_create_sticker_with_owned_album(
    authenticated_client,
    db_session,
    demo_user,
):
    album = create_album_in_db(db_session, demo_user)
    new_sticker_data = {
        "name": "Di Maria",
        "collection_name": "Argentina 2026",
        "role": "Extremo",
        "number": 11,
        "image_url": "http://example.com/di-maria.png",
        "is_favorite": False,
        "album_id": album.id,
    }

    response = authenticated_client.post("/api/stickers/", json=new_sticker_data)

    assert response.status_code == 201
    created_sticker = response.json()
    assert created_sticker["name"] == new_sticker_data["name"]
    assert created_sticker["album_id"] == album.id


def test_create_sticker_with_missing_album_returns_404(authenticated_client):
    response = authenticated_client.post(
        "/api/stickers/",
        json={
            "name": "Dibu Martinez",
            "collection_name": "Argentina 2026",
            "role": "Arquero",
            "number": 23,
            "image_url": "http://example.com/dibu.png",
            "is_favorite": True,
            "album_id": 9999,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Album not found"}


def test_create_sticker_with_another_users_album_returns_403(
    authenticated_client,
    db_session,
):
    other_user = create_user_in_db(db_session, "otheruser")
    other_album = create_album_in_db(db_session, other_user)

    response = authenticated_client.post(
        "/api/stickers/",
        json={
            "name": "Julian Alvarez",
            "collection_name": "Argentina 2026",
            "role": "Delantero",
            "number": 9,
            "image_url": "http://example.com/julian.png",
            "is_favorite": False,
            "album_id": other_album.id,
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Cannot add sticker to an album you do not own"
    }
