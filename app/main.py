import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.routers import albums, pages, stickers
from app.startup import init_db


def create_lifespan(init_database: bool):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if init_database:
            init_db()
        yield

    return lifespan


def create_app(init_database: bool = True) -> FastAPI:
    app = FastAPI(lifespan=create_lifespan(init_database))

    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv("SESSION_SECRET_KEY", "dev-secret-change-me"),
        same_site="lax",
        https_only=False,
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(pages.router)
    app.include_router(albums.router)
    app.include_router(stickers.router)

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
