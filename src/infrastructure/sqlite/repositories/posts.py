from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import AlreadyExistsException, InfrastructureException
from src.infrastructure.sqlite.models.posts import Post
from src.schemas.posts import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Post]:
        try:
            result = await self.session.execute(
                select(Post).options(selectinload(Post.images))
            )
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении постов: {str(e)}")

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        try:
            result = await self.session.execute(
                select(Post)
                .where(Post.id == post_id)
                .options(selectinload(Post.images))
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении поста: {str(e)}")

    async def create(self, data: PostCreate) -> Post:
        try:
            post = Post(**data.model_dump())
            self.session.add(post)
            await self.session.flush()
            await self.session.refresh(post)
            return post
        except IntegrityError as e:
            raise AlreadyExistsException(
                f"Пост с таким slug или данными уже существует: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании поста: {str(e)}")

    async def update(self, post_id: int, data: PostUpdate) -> Optional[Post]:
        try:
            result = await self.session.execute(select(Post).where(Post.id == post_id))
            post = result.scalar_one_or_none()
            if not post:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(post, key, value)
            await self.session.flush()
            await self.session.refresh(post)
            return post
        except IntegrityError as e:
            raise AlreadyExistsException(f"Конфликт данных при обновлении поста: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении поста: {str(e)}")

    async def delete(self, post_id: int) -> bool:
        try:
            result = await self.session.execute(select(Post).where(Post.id == post_id))
            post = result.scalar_one_or_none()
            if not post:
                return False
            await self.session.delete(post)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении поста: {str(e)}")
