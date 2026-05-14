from fastapi import APIRouter, status
from typing import List
from src.schemas.comments import CommentCreate, CommentUpdate, CommentOut
from src.domain.use_cases.comments import CommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])
use_case = CommentUseCase()

@router.get("/", response_model=List[CommentOut])
async def get_all_comments():
    return use_case.get_all()

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate):
    return use_case.create_comment(comment_data)

@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(comment_id: int, comment_data: CommentUpdate):
    return use_case.update_comment(comment_id, comment_data)

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int):
    use_case.delete_comment(comment_id)
    return {"detail": f"Комментарий {comment_id} успешно удалён"}