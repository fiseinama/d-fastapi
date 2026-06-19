from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, InfrastructureException
from src.infrastructure.sqlite.models.users import User
from src.schemas.users import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[User]:
        try:
            result = await self.session.execute(select(User))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении списка пользователей: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[User]:
        try:
            result = await self.session.execute(select(User).where(User.id == id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при поиске пользователя по ID: {str(e)}")

    async def get_by_username(self, username: str) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при поиске пользователя по имени: {str(e)}")

    async def create(self, data: UserCreate) -> User:
        try:
            user = User(**data.model_dump())
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise AlreadyExistsException("Пользователь с таким именем или email уже существует")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании пользователя: {str(e)}")

    async def update(self, id: int, data: UserUpdate) -> Optional[User]:
        try:
            result = await self.session.execute(select(User).where(User.id == id))
            user = result.scalar_one_or_none()
            if not user:
                return None

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)

            await self.session.flush()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise AlreadyExistsException("Конфликт данных при обновлении")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении пользователя: {str(e)}")

    async def delete(self, id: int) -> bool:
        try:
            result = await self.session.execute(select(User).where(User.id == id))
            user = result.scalar_one_or_none()
            if not user:
                return False
            await self.session.delete(user)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении пользователя: {str(e)}")
