from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user, get_db
from src.domain.use_cases.comments import CommentUseCase
from src.infrastructure.sqlite.models.users import User
from src.schemas.comments import CommentOut

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_comment_use_case(db: AsyncSession = Depends(get_db)) -> CommentUseCase:
    return CommentUseCase(db)


@router.get("/", response_model=List[CommentOut])
async def get_all_comments(use_case: CommentUseCase = Depends(get_comment_use_case)):
    return await use_case.get_all()


@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(
    comment_id: int,
    use_case: CommentUseCase = Depends(get_comment_use_case),
):
    return await use_case.get_by_id(comment_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    image_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    use_case: CommentUseCase = Depends(get_comment_use_case),
):
    return await use_case.create_comment(
        text=text,
        post_id=post_id,
        author_id=current_user,
        image_file=image_file,
    )


@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(
    comment_id: int,
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user=Depends(get_current_user),
    use_case: CommentUseCase = Depends(get_comment_use_case),
):
    return await use_case.update_comment(
        comment_id=comment_id,
        text=text,
        image_file=image,
        user_id=current_user.id,
    )


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user=Depends(get_current_user),
    use_case: CommentUseCase = Depends(get_comment_use_case),
):
    await use_case.delete_comment(comment_id, user_id=current_user.id)
    return {"detail": f"Комментарий {comment_id} успешно удалён"}
