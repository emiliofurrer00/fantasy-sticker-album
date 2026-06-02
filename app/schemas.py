from pydantic import BaseModel, Field, HttpUrl


class StickerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    collection_name: str | None = Field(min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=50)
    number: int | None = Field(default=None, ge=1)
    image_url: HttpUrl | None = None
    is_favorite: bool = False
    album_id: int | None = None

class StickerRead(BaseModel):
    id: int
    name: str
    collection_name: str | None
    role: str | None
    number: int | None
    image_url: HttpUrl | None
    is_favorite: bool
    album_id: int | None
    model_config = {
        "from_attributes": True,
    }


class AlbumCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    is_public: bool = False


class AlbumRead(BaseModel):
    id: int
    title: str
    description: str | None
    is_public: bool
    owner_id: int

    model_config = {
        "from_attributes": True,
    }
