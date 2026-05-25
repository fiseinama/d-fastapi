from fastapi import APIRouter, status, Depends, File, Form, UploadFile
from typing import List, Optional
from src.schemas.posts import PostCreate, PostUpdate, PostOut
from src.domain.use_cases.posts import PostUseCase
from src.api.dependencies import get_current_user
from datetime import datetime
from src.infrastructure.sqlite.models.users import User

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
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    category_id: int = Form(...),
    location_id: Optional[int] = Form(None),
    pub_date: Optional[datetime] = Form(None),
    is_published: bool = Form(True),
    image_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    use_case: PostUseCase = Depends(PostUseCase)
):
    return await use_case.create_post(
        title=title,
        text=text,
        category_id=category_id,
        author_id=current_user.id,
        location_id=location_id,
        pub_date=pub_date,
        is_published=is_published,
        image_file=image_file
    )

@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    title: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    location_id: Optional[int] = Form(None),
    pub_date: Optional[datetime] = Form(None),
    is_published: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_user)
):
    return await use_case.update_post(
        post_id=post_id,
        title=title,
        text=text,
        category_id=category_id,
        location_id=location_id,
        pub_date=pub_date,
        is_published=is_published,
        image_file=image,
        user_id=current_user.id
    )

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user = Depends(get_current_user)
):
    use_case.delete_post(post_id, user_id=current_user.id)
    return {"detail": f"Пост {post_id} успешно удалён"}

