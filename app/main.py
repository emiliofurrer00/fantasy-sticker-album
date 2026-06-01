from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine, get_db
from app.routers import pages
from app.seed import seed_data

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)
seed_data(SessionLocal())

app.include_router(pages.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
