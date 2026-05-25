from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import asyncio
import uvicorn
from fastapi.staticfiles import StaticFiles
from src.app import create_app
from src.infrastructure.sqlite.database import engine, Base

# Импорты моделей необходимы для работы SQLAlchemy
from src.infrastructure.sqlite.models.users import User
from src.infrastructure.sqlite.models.posts import Post
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.models.location import Location

app = create_app()
app.mount("/static", StaticFiles(directory="static"), name="static")

async def run() -> None:
    # Base.metadata.create_all(bind=engine)
    config = uvicorn.Config(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())