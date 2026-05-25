import os
import uuid
from typing import Optional
from fastapi import UploadFile

from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.schemas.comments import CommentCreate, CommentUpdate

# используем ту же директорию для загрузки файлов
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_uploaded_file(file: Optional[UploadFile]) -> Optional[str]:
    """сохраняет загруженный файл на диск и возвращает путь к нему"""
    if not file or not file.filename:
        return None

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path


class CommentUseCase:
    def __init__(self):
        self.repo = CommentRepository()

    def get_all(self):
        """получает список всех комментариев в системе"""
        return self.repo.get_all()

    async def create_comment(
            self, text: str, post_id: int, author_id: int, image_file: Optional[UploadFile] = None
    ):
        """публикует новый комментарий к посту с возможностью прикрепить картинку"""
        try:
            # сохраняем файл изображения для комментария, если он передан
            image_path = await save_uploaded_file(image_file)

            # собираем объект для создания записи
            comment_data = CommentCreate(
                text=text,
                post_id=post_id,
                author_id=author_id,
                image=image_path
            )
            return self.repo.create(comment_data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось опубликовать комментарий: {e.message}")

    async def update_comment(
            self, comment_id: int, user_id: int, text: Optional[str] = None, image_file: Optional[UploadFile] = None
    ):
        """обновляет текст или изображение существующего комментария"""
        update_dict = {}
        if text is not None:
            update_dict["text"] = text

        # если передана новая картинка, обновляем её файл на диске
        if image_file:
            image_path = await save_uploaded_file(image_file)
            update_dict["image"] = image_path

        update_data = CommentUpdate(**update_dict)
        comment = self.repo.update(comment_id, update_data)
        if not comment:
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден для обновления")
        return comment

    def delete_comment(self, comment_id: int, user_id: int):
        """удаляет выбранный комментарий по его идентификатору"""
        if not self.repo.delete(comment_id):
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден")
        return True