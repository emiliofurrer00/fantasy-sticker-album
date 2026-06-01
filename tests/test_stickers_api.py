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
        "is_favorite": True
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

def test_create_sticker_validates_payload(authenticated_client):
    invalid_sticker_data = {
        "name": "",  # Invalido
        "collection_name": "Argentina 2026",
        "role": "Delantero",
        "number": 10,
        "image_url": "not-a-valid-url",  # Invalido
        "is_favorite": True
    }
    
    response = authenticated_client.post("/api/stickers/", json=invalid_sticker_data)
    
    assert response.status_code == 422
    errors = response.json()
    assert len(errors["detail"]) == 2 