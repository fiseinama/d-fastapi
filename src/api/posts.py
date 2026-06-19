from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user, get_db
from src.domain.use_cases.posts import PostUseCase
from src.infrastructure.sqlite.models.users import User
from src.schemas.posts import PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])


def get_post_use_case(db: AsyncSession = Depends(get_db)) -> PostUseCase:
    return PostUseCase(db)


@router.get("/", response_model=List[PostOut])
async def get_all_posts(use_case: PostUseCase = Depends(get_post_use_case)):
    return await use_case.get_all()


@router.get("/{post_id}", response_model=PostOut)
async def get_one_post(
    post_id: int,
    use_case: PostUseCase = Depends(get_post_use_case),
):
    return await use_case.get_by_id(post_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    category_id: int = Form(...),
    location_id: Optional[int] = Form(None),
    pub_date: Optional[datetime] = Form(None),
    is_published: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    use_case: PostUseCase = Depends(get_post_use_case),
):
    # отрезаем часовой пояс для Postgres
    if pub_date and pub_date.tzinfo is not None:
        pub_date = pub_date.replace(tzinfo=None)

    return await use_case.create_post(
        title=title,
        text=text,
        category_id=category_id,
        author_id=current_user,
        location_id=location_id,
        pub_date=pub_date,
        is_published=is_published,
        image_file=image,
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
    current_user=Depends(get_current_user),
    use_case: PostUseCase = Depends(get_post_use_case),
):
    # отрезаем часовой пояс для Postgres
    if pub_date and pub_date.tzinfo is not None:
        pub_date = pub_date.replace(tzinfo=None)

    return await use_case.update_post(
        post_id=post_id,
        title=title,
        text=text,
        category_id=category_id,
        location_id=location_id,
        pub_date=pub_date,
        is_published=is_published,
        image_file=image,
        user_id=current_user,
    )


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user=Depends(get_current_user),
    use_case: PostUseCase = Depends(get_post_use_case),
):
    await use_case.delete_post(post_id, user_id=current_user)
    return {"detail": f"Пост {post_id} успешно удалён"}