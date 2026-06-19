import os
import uuid
import aiofiles
from typing import List, Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comments import CommentCreate, CommentUpdate

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_uploaded_file(file: Optional[UploadFile]) -> Optional[str]:
    if not file or not file.filename:
        return None

    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        contents = await file.read()

        # 🔥 ИСПРАВЛЕНИЕ: Перевели запись файла на асинхронные рельсы
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)  # <-- Тут обязательно должен быть await!

        return file_path
    except Exception:
        return None


class CommentUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session  # Сохраняем сессию для проверок в репозиториях
        self.repo = CommentRepository(session)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, comment_id: int):
        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден")
        return comment

    async def create_comment(
            self, text: str, post_id: int, author_id: int, image_file: Optional[UploadFile] = None
    ):
        # 1. Проверяем, существует ли пост, к которому пишется комментарий
        from src.infrastructure.sqlite.repositories.posts import PostRepository
        post_repo = PostRepository(self.session)

        post = await post_repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден. Комментарий не может быть опубликован.")

        try:
            image_path = await save_uploaded_file(image_file)

            comment_data = CommentCreate(
                text=text,
                post_id=post_id,
                author_id=author_id,
                image=image_path,
            )
            return await self.repo.create(comment_data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось опубликовать комментарий: {e.message}")

    async def update_comment(
            self,
            comment_id: int,
            user_id: int,
            text: Optional[str] = None,
            image_file: Optional[UploadFile] = None,
    ):
        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден для обновления")

        if comment.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете редактировать чужой комментарий!",
            )

        update_dict = {}
        if text is not None:
            update_dict["text"] = text

        if image_file:
            image_path = await save_uploaded_file(image_file)
            update_dict["image"] = image_path

        update_data = CommentUpdate(**update_dict)
        comment = await self.repo.update(comment_id, update_data)
        if not comment:
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден для обновления")
        return comment

    async def delete_comment(self, comment_id: int, user_id: int):
        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден")

        if comment.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете удалить чужой комментарий!",
            )

        await self.repo.delete(comment_id)
        return True