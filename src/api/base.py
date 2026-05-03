from fastapi import APIRouter, status, HTTPException
from src.schemas.posts import PostOut   # ← исправлено

router = APIRouter(prefix="/base", tags=["Base"])


@router.get("/hello_world", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    return {"text": "Hello, World!"}


@router.post("/test_json", status_code=status.HTTP_201_CREATED)
async def test_json(post: PostOut) -> dict:      # ← используем PostOut
    response = {
        "post_text": post.text,
        "author_id": post.author_id,             # author.login пока нет
    }
    return response