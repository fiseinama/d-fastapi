from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.base import router as base_router
from src.api.posts import router as posts_router
from src.api.categories import router as categories_router   # добавь


def create_app() -> FastAPI:
    app = FastAPI(
        title="Blogicum API",
        root_path="/api/v1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router)
    app.include_router(posts_router)
    app.include_router(categories_router)

    return app