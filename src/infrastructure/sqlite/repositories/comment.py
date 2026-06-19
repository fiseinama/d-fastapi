from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, InfrastructureException
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Comment]:
        try:
            result = await self.session.execute(select(Comment))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении комментариев: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[Comment]:
        try:
            result = await self.session.execute(select(Comment).where(Comment.id == id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении комментария: {str(e)}")

    async def create(self, data: CommentCreate) -> Comment:
        try:
            comment = Comment(**data.model_dump())
            self.session.add(comment)
            await self.session.flush()
            await self.session.refresh(comment)
            return comment
        except IntegrityError as e:
            raise AlreadyExistsException(
                f"Комментарий уже существует или нарушены связи: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании комментария: {str(e)}")

    async def update(self, id: int, data: CommentUpdate) -> Optional[Comment]:
        try:
            result = await self.session.execute(select(Comment).where(Comment.id == id))
            comment = result.scalar_one_or_none()
            if not comment:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(comment, key, value)
            await self.session.flush()
            await self.session.refresh(comment)
            return comment
        except IntegrityError as e:
            raise AlreadyExistsException(f"Ошибка обновления: данные конфликтуют: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка комментария: {str(e)}")

    async def delete(self, id: int) -> bool:
        try:
            result = await self.session.execute(select(Comment).where(Comment.id == id))
            comment = result.scalar_one_or_none()
            if not comment:
                return False
            await self.session.delete(comment)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении комментария: {str(e)}")
