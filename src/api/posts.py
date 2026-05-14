from fastapi import APIRouter, status
from typing import List
from src.schemas.posts import PostCreate, PostUpdate, PostOut
from src.domain.use_cases.posts import PostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])
use_case = PostUseCase()

@router.get("/", response_model=List[PostOut])
async def get_all_posts():
    return use_case.get_all()

@router.get("/{post_id}", response_model=PostOut)
async def get_one_post(post_id: int):
    return use_case.get_by_id(post_id)

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    return use_case.create_post(post_data)

@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post_data: PostUpdate):
    return use_case.update_post(post_id, post_data)

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    use_case.delete_post(post_id)
    return {"detail": f"Пост {post_id} успешно удалён"}