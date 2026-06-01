from pydantic import BaseModel, HttpUrl, Field

class StickerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    collection_name: str | None = Field(min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=50)
    number: int | None = Field(default=None, ge=1)
    image_url: HttpUrl | None = None
    is_favorite: bool = False

class StickerRead(BaseModel):
    id: int
    name: str
    collection_name: str | None
    role: str | None
    number: int | None
    image_url: HttpUrl | None
    is_favorite: bool

    model_config = {
        "from_attributes": True,
    }
    