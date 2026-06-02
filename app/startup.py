from app.database import Base, SessionLocal, engine
from app.seed import seed_data


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
