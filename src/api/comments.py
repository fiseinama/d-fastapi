from fastapi import APIRouter, status, Depends, Form, File, UploadFile
from typing import List, Optional
from src.schemas.comments import CommentCreate, CommentUpdate, CommentOut
from src.domain.use_cases.comments import CommentUseCase
from src.api.dependencies import get_current_user
from src.infrastructure.sqlite.models.users import User

router = APIRouter(prefix="/comments", tags=["Comments"])
use_case = CommentUseCase()

@router.get("/", response_model=List[CommentOut])
async def get_all_comments():
    return use_case.get_all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    image_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    use_case: CommentUseCase = Depends(CommentUseCase)
):
    return await use_case.create_comment(
        text=text,
        post_id=post_id,
        author_id=current_user.id,
        image_file=image_file
    )


@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(
    comment_id: int,
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_user)
):
    return await use_case.update_comment(
        comment_id=comment_id,
        text=text,
        image_file=image,
        user_id=current_user.id
    )

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user = Depends(get_current_user)
):
    use_case.delete_comment(comment_id)
    return {"detail": f"Комментарий {comment_id} успешно удалён"}