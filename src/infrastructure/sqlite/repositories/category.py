from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, InfrastructureException
from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Category]:
        try:
            result = await self.session.execute(select(Category))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении категорий: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[Category]:
        try:
            result = await self.session.execute(select(Category).where(Category.id == id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении категории: {str(e)}")

    async def create(self, data: CategoryCreate) -> Category:
        try:
            category = Category(**data.model_dump())
            self.session.add(category)
            await self.session.flush()
            await self.session.refresh(category)
            return category
        except IntegrityError as e:
            raise AlreadyExistsException(
                f"Категория с такими данными уже существует: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании категории: {str(e)}")

    async def update(self, id: int, data: CategoryUpdate) -> Optional[Category]:
        try:
            result = await self.session.execute(select(Category).where(Category.id == id))
            category = result.scalar_one_or_none()
            if not category:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(category, key, value)
            await self.session.flush()
            await self.session.refresh(category)
            return category
        except IntegrityError as e:
            raise AlreadyExistsException(f"Ошибка обновления: данные уже заняты: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении категории: {str(e)}")

    async def delete(self, id: int) -> bool:
        try:
            result = await self.session.execute(select(Category).where(Category.id == id))
            category = result.scalar_one_or_none()
            if not category:
                return False
            await self.session.delete(category)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении категории: {str(e)}")
