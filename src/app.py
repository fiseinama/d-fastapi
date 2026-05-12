from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.posts import router as posts_router
from src.api.categories import router as categories_router
from src.api.comments import router as comments_router
from src.api.users import router as users_router
from src.api.location import router as location_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Blogicum API",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(posts_router, prefix="/api/v1")
    app.include_router(categories_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(comments_router, prefix="/api/v1")
    app.include_router(location_router, prefix="/api/v1")

    return app