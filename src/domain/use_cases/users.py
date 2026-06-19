from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.core.security import hash_password
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.users import UserCreate, UserUpdate


class UserUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"Пользователь с ID {user_id} не найден")
        return user

    async def create_user(self, data: UserCreate):
        if await self.repo.get_by_username(data.username):
            raise AlreadyExistsException(f"Пользователь '{data.username}' уже зарегистрирован")

        try:
            data.password = hash_password(data.password)
            return await self.repo.create(data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать аккаунт: {e.message}")

    async def update_user(self, user_id: int, data: UserUpdate):
        if data.password is not None:
            data.password = hash_password(data.password)

        user = await self.repo.update(user_id, data)
        if not user:
            raise NotFoundException(f"Пользователь с ID {user_id} не найден")
        return user

    async def delete_user(self, user_id: int):
        if not await self.repo.delete(user_id):
            raise NotFoundException(f"Не удалось удалить: пользователь {user_id} не найден")
        return True
