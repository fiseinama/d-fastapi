from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from src.api.posts import router as posts_router
from src.api.categories import router as categories_router
from src.api.comments import router as comments_router
from src.api.users import router as users_router
from src.api.location import router as location_router
from src.api.auth import router as auth_router

from src.core.exceptions import NotFoundException, AlreadyExistsException, InfrastructureException, UnauthorizedException

def create_app() -> FastAPI:
    app = FastAPI(
        title="Blogicum API",
        version="1.0.0"
    )

    # Регистрация обработчиков ошибок
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @app.exception_handler(InfrastructureException)
    async def infrastructure_exception_handler(request: Request, exc: InfrastructureException):
        return JSONResponse(status_code=500, content={"detail": f"Ошибка сервера: {exc.message}"})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(auth_router, prefix="/api/v1")

    app.include_router(posts_router, prefix="/api/v1")
    app.include_router(categories_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(comments_router, prefix="/api/v1")
    app.include_router(location_router, prefix="/api/v1")

    return app
app = create_app()