from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    stickers: Mapped[list["Sticker"]] = relationship(
        "Sticker", back_populates="owner", cascade="all, delete-orphan")

class Sticker(Base):
    __tablename__ = "stickers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    collection_name: Mapped[str | None] = mapped_column(index=True, nullable=True)
    role: Mapped[str | None] = mapped_column(index=True, nullable=True)
    number: Mapped[int | None] = mapped_column(index=True, nullable=True)
    image_url: Mapped[str | None] = mapped_column(nullable=True)
    is_favorite: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="stickers")