from fastapi import APIRouter, HTTPException, status
from typing import List

from src.schemas.posts import PostCreate, PostUpdate, PostOut
from src.infrastructure.sqlite.repositories.posts import PostRepository

router = APIRouter(prefix="/posts", tags=["Posts"])

# иниц репозиторий
post_repo = PostRepository()


@router.get("/", response_model=List[PostOut])
async def get_all_posts():
    return post_repo.get_all()


@router.get("/{post_id}", response_model=PostOut)
async def get_one_post(post_id: int):
    post = post_repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    return post_repo.create(post_data)


@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post_data: PostUpdate):
    post = post_repo.update(post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    success = post_repo.delete(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return {"detail": f"Пост {post_id} успешно удалён"}