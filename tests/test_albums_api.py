from app.models import Album


def create_album_in_db(db_session, owner, *, is_public: bool) -> Album:
    album = Album(
        title="Album test",
        description="Fixture de album",
        is_public=is_public,
        owner_id=owner.id,
    )
    db_session.add(album)
    db_session.commit()
    db_session.refresh(album)
    return album


def test_create_album_requires_authentication(client):
    response = client.post(
        "/api/albums/",
        json={
            "title": "Mi album",
            "description": "Album privado",
            "is_public": False,
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_album(authenticated_client):
    response = authenticated_client.post(
        "/api/albums/",
        json={
            "title": "Mundial 2026",
            "description": "Figuritas favoritas",
            "is_public": True,
        },
    )

    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "Mundial 2026"
    assert data["description"] == "Figuritas favoritas"
    assert data["is_public"] is True
    assert "id" in data
    assert "owner_id" in data


def test_anonymous_user_can_read_public_album(client, db_session, demo_user):
    album = create_album_in_db(db_session, demo_user, is_public=True)

    response = client.get(f"/api/albums/{album.id}")

    assert response.status_code == 200
    assert response.json()["id"] == album.id
    assert response.json()["is_public"] is True


def test_anonymous_user_cannot_read_private_album(client, db_session, demo_user):
    album = create_album_in_db(db_session, demo_user, is_public=False)

    response = client.get(f"/api/albums/{album.id}")

    assert response.status_code == 403
    assert response.json() == {"detail": "Album is private"}


def test_owner_can_read_private_album(authenticated_client, db_session, demo_user):
    album = create_album_in_db(db_session, demo_user, is_public=False)

    response = authenticated_client.get(f"/api/albums/{album.id}")

    assert response.status_code == 200
    assert response.json()["id"] == album.id
    assert response.json()["is_public"] is False


def test_list_public_albums_only_returns_public_albums(client, db_session, demo_user):
    public_album = create_album_in_db(db_session, demo_user, is_public=True)
    private_album = create_album_in_db(db_session, demo_user, is_public=False)

    response = client.get("/api/albums/public")

    album_ids = {album["id"] for album in response.json()}
    assert response.status_code == 200
    assert public_album.id in album_ids
    assert private_album.id not in album_ids


def test_list_my_albums_returns_owned_albums(
    authenticated_client,
    db_session,
    demo_user,
):
    album = create_album_in_db(db_session, demo_user, is_public=False)

    response = authenticated_client.get("/api/albums/me")

    album_ids = {album_data["id"] for album_data in response.json()}
    assert response.status_code == 200
    assert album.id in album_ids
