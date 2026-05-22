from fastapi import APIRouter, status, Depends
from typing import List
from src.schemas.posts import PostCreate, PostUpdate, PostOut
from src.domain.use_cases.posts import PostUseCase
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])
use_case = PostUseCase()

# роуты, которые будут доступны всем (и неавторизованным пользователям)
@router.get("/", response_model=List[PostOut])
async def get_all_posts():
    return use_case.get_all()

@router.get("/{post_id}", response_model=PostOut)
async def get_one_post(post_id: int):
    return use_case.get_by_id(post_id)

# защищенные роуты (только для авторизованных)
@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user = Depends(get_current_user)
):
    return use_case.create_post(post_data, author_id=current_user.id)

@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user = Depends(get_current_user)
):
    return use_case.update_post(post_id, post_data, user_id=current_user.id)

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user = Depends(get_current_user)
):
    use_case.delete_post(post_id, user_id=current_user.id)
    return {"detail": f"Пост {post_id} успешно удалён"}