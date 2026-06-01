from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password
from app.crud import get_user_by_username


# Funcion para seedear db. A reemplazarse con un script de seedeo o migraciones
def seed_data(db: Session) -> None:
    existing_demo_user = get_user_by_username(db, "demouser")
    try: 
        if not existing_demo_user:
            demouser = models.User(
                username="demouser",
                password_hash=hash_password("demouser123")
            )
            db.add(demouser)
            db.commit()
            db.refresh(demouser)
            demo_stickers = [
                models.Sticker(
                    name="Sticker 1",
                    collection_name="Colección A",
                    role="Jugador",
                    number=1,
                    image_url="https://static.wikia.nocookie.net/theoffice/images/b/be/Character_-_MichaelScott.PNG/revision/latest?cb=20200413224550",
                    owner_id=demouser.id
                ),
                models.Sticker(
                    name="Sticker 2",
                    collection_name="Colección A",
                    role="Portero",
                    number=2,
                    image_url="https://static.wikia.nocookie.net/theoffice/images/c/c5/Dwight_.jpg/revision/latest/scale-to-width-down/1000?cb=20170701082424",
                    owner_id=demouser.id
                ),
            ]
            db.add_all(demo_stickers)
            db.commit()
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()