import os
import uuid
import aiofiles
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.infrastructure.sqlite.repositories.post_image import PostImageRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.posts import PostCreate, PostUpdate

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_uploaded_file(file: Optional[UploadFile]) -> Optional[str]:
    if file is None or not file.filename or file.filename.strip() == "":
        return None

    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        contents = await file.read()
        if not contents:
            return None

        # <-- 2. ЗАМЕНИЛИ ОБЫЧНЫЙ OPEN НА АСИНХРОННЫЙ AIOFILES
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)  # <-- ОБЯЗАТЕЛЬНО С await!

        return file_path
    except Exception:
        return None


class PostUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session  # Сохраняем сессию для создания других репозиториев
        self.repo = PostRepository(session)
        self.image_repo = PostImageRepository(session)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, post_id: int):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")
        return post

    async def create_post(
        self,
        title: str,
        text: str,
        category_id: int,
        author_id: int,
        location_id: Optional[int] = None,
        pub_date: Optional[datetime] = None,
        is_published: bool = True,
        image_file: Optional[UploadFile] = None,
    ):
        # Импортируем другие репозитории внутри метода, чтобы избежать циклического импорта
        from src.infrastructure.sqlite.repositories.category import CategoryRepository
        from src.infrastructure.sqlite.repositories.location import LocationRepository

        category_repo = CategoryRepository(self.session)
        location_repo = LocationRepository(self.session)

        # 1. Проверяем существование категории
        category = await category_repo.get_by_id(category_id)
        if not category:
            raise NotFoundException(f"Категория с ID {category_id} не найдена. Пост не может быть создан.")

        # 2. Проверяем существование локации (если она передана и не равна 0/None)
        if location_id is not None and location_id != 0:
            location = await location_repo.get_by_id(location_id)
            if not location:
                raise NotFoundException(f"Локация с ID {location_id} не найдена. Пост не может быть создан.")

        try:
            # Безопасно получаем путь (будет None, если картинку не прикрепили)
            main_image = await save_uploaded_file(image_file)

            post_data = PostCreate(
                title=title,
                text=text,
                image=main_image,
                pub_date=pub_date,
                is_published=is_published,
                author_id=author_id,
                category_id=category_id,
                location_id=location_id,
            )
            post = await self.repo.create(post_data)
            return post

        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать пост '{title}': {e.message}")

    async def update_post(
        self,
        post_id: int,
        user_id: int,
        title: Optional[str] = None,
        text: Optional[str] = None,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None,
        pub_date: Optional[datetime] = None,
        is_published: Optional[bool] = None,
        image_file: Optional[UploadFile] = None,
    ):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")

        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете редактировать чужой пост!",
            )

        # Проверки при обновлении данных (если передаются новые ID)
        if category_id is not None:
            from src.infrastructure.sqlite.repositories.categories import CategoryRepository
            category_repo = CategoryRepository(self.session)
            category = await category_repo.get_by_id(category_id)
            if not category:
                raise NotFoundException(f"Категория с ID {category_id} не найдена.")

        if location_id is not None and location_id != 0:
            from src.infrastructure.sqlite.repositories.locations import LocationRepository
            location_repo = LocationRepository(self.session)
            location = await location_repo.get_by_id(location_id)
            if not location:
                raise NotFoundException(f"Локация с ID {location_id} не найдена.")

        update_dict = {}
        if title is not None:
            update_dict["title"] = title
        if text is not None:
            update_dict["text"] = text
        if category_id is not None:
            update_dict["category_id"] = category_id
        if location_id is not None:
            update_dict["location_id"] = location_id
        if pub_date is not None:
            update_dict["pub_date"] = pub_date
        if is_published is not None:
            update_dict["is_published"] = is_published

        # Безопасное обновление картинки
        image_path = await save_uploaded_file(image_file)
        if image_path:
            update_dict["image"] = image_path

        update_data = PostUpdate(**update_dict)
        return await self.repo.update(post_id, update_data)

    async def delete_post(self, post_id: int, user_id: int):
        post = await self.repo.get_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")

        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете удалить чужой пост!",
            )
        await self.repo.delete(post_id)
        return True