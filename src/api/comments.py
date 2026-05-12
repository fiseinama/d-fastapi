from fastapi import APIRouter, HTTPException, status
from typing import List

from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentCreate, CommentUpdate, CommentOut

router = APIRouter(prefix="/comments", tags=["Comments"])
repo = CommentRepository()

@router.get("/", response_model=List[CommentOut])
async def get_all_comments():
    return repo.get_all()

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate):
    return repo.create(comment_data)

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int):
    success = repo.delete(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return {"detail": f"Комментарий {comment_id} успешно удалён"}