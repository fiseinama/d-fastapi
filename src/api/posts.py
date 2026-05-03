from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from src.schemas.posts import PostCreate, PostUpdate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])

db_posts: List[PostOut] = []


@router.get("/", response_model=List[PostOut])
async def get_all_posts():
    return db_posts


@router.get("/{post_id}", response_model=PostOut)
async def get_one_post(post_id: int):
    for post in db_posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Пост не найден")


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    new_id = len(db_posts) + 1
    new_post = PostOut(
        id=new_id,
        created_at=datetime.now(),
        **post_data.model_dump()
    )
    db_posts.append(new_post)
    return new_post


@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post_data: PostUpdate):
    for index, post in enumerate(db_posts):
        if post.id == post_id:
            update_dict = post_data.model_dump(exclude_unset=True)
            updated_data = post.model_dump()
            updated_data.update(update_dict)
            db_posts[index] = PostOut(**updated_data)
            return db_posts[index]
    raise HTTPException(status_code=404, detail="Пост не найден")


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    for index, post in enumerate(db_posts):
        if post.id == post_id:
            db_posts.pop(index)
            return {"detail": f"Пост {post_id} успешно удалён"}
    raise HTTPException(status_code=404, detail="Пост не найден")