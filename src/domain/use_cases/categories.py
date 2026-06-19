from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.categories import CategoryCreate, CategoryUpdate


class CategoryUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = CategoryRepository(session)

    async def create_category(self, data: CategoryCreate):
        try:
            return await self.repo.create(data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать категорию '{data.title}': {e.message}")

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, category_id: int):
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException(f"Категория с ID {category_id} не существует")
        return category

    async def update_category(self, category_id: int, data: CategoryUpdate):
        category = await self.repo.update(category_id, data)
        if not category:
            raise NotFoundException(f"Не удалось обновить: категория {category_id} не найдена")
        return category

    async def delete_category(self, category_id: int):
        if not await self.repo.delete(category_id):
            raise NotFoundException(f"Удаление невозможно: категория {category_id} не найдена")
        return True
