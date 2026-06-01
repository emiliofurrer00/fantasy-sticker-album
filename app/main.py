import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, SessionLocal, engine, get_db
from app.routers import pages
from app.seed import seed_data

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "dev-secret-change-me"),
    same_site="lax",
    https_only=False,
)
   
app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)
seed_data(SessionLocal())

app.include_router(pages.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
