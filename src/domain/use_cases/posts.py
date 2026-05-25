import os
import uuid
from typing import Optional
from datetime import datetime
from fastapi import UploadFile, HTTPException, status

from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.schemas.posts import PostCreate, PostUpdate

# папка для сохранения картинок внутри контейнера
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_uploaded_file(file: Optional[UploadFile]) -> Optional[str]:
    """сохраняет загруженный файл на диск и возвращает путь к нему"""
    if not file or not file.filename:
        return None

    # генерируем уникальное имя файла для предотвращения перезаписи
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # асинхронное чтение файла и запись на диск
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path


class PostUseCase:
    def __init__(self):
        self.repo = PostRepository()

    def get_all(self):
        """получает список всех существующих постов"""
        return self.repo.get_all()

    def get_by_id(self, post_id: int):
        """находит один пост по его идентификатору"""
        post = self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")
        return post

    async def create_post(
            self, title: str, text: str, category_id: int, author_id: int,
            location_id: Optional[int] = None, pub_date: Optional[datetime] = None,
            is_published: bool = True, image_file: Optional[UploadFile] = None
    ):
        """создает новый пост, предварительно сохраняя прикрепленное изображение"""
        try:
            # сохраняем картинку на диск, если она прикреплена к посту
            image_path = await save_uploaded_file(image_file)

            # собираем и валидируем данные через pydantic-схему
            post_data = PostCreate(
                title=title,
                text=text,
                image=image_path,
                pub_date=pub_date,
                is_published=is_published,
                author_id=author_id,
                category_id=category_id,
                location_id=location_id
            )
            return self.repo.create(post_data)

        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать пост '{title}': {e.message}")

    async def update_post(
            self, post_id: int, user_id: int, title: Optional[str] = None,
            text: Optional[str] = None, category_id: Optional[int] = None,
            location_id: Optional[int] = None, pub_date: Optional[datetime] = None,
            is_published: Optional[bool] = None, image_file: Optional[UploadFile] = None
    ):
        """обновляет данные поста после проверки прав автора и валидации изменений"""
        post = self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")

        # проверяем, является ли пользователь автором этого поста
        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете редактировать чужой пост!"
            )

        # формируем словарь только со значениями, переданными для обновления
        update_dict = {}
        if title is not None: update_dict["title"] = title
        if text is not None: update_dict["text"] = text
        if category_id is not None: update_dict["category_id"] = category_id
        if location_id is not None: update_dict["location_id"] = location_id
        if pub_date is not None: update_dict["pub_date"] = pub_date
        if is_published is not None: update_dict["is_published"] = is_published

        # если загружена новая картинка, сохраняем её и обновляем путь
        if image_file:
            image_path = await save_uploaded_file(image_file)
            update_dict["image"] = image_path

        # валидация обновленных полей через pydantic
        update_data = PostUpdate(**update_dict)
        return self.repo.update(post_id, update_data)

    def delete_post(self, post_id: int, user_id: int):
        """удаляет пост, если текущий пользователь является его автором"""
        post = self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")

        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете удалить чужой пост!"
            )
        self.repo.delete(post_id)
        return True