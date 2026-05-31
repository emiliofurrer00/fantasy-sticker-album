from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    stickers = relationship("Sticker", back_populates="owner")

class Sticker(Base):
    __tablename__ = "stickers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    collection_name = Column(String, index=True, nullable=True)
    role = Column(String, index=True, nullable=True)
    number = Column(Integer, index=True, nullable=True)
    image_url = Column(String, nullable=True)
    is_favorite = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="stickers")