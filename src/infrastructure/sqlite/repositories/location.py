from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, InfrastructureException
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationCreate, LocationUpdate


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Location]:
        try:
            result = await self.session.execute(select(Location))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении локаций: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[Location]:
        try:
            result = await self.session.execute(select(Location).where(Location.id == id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении локации: {str(e)}")

    async def create(self, data: LocationCreate) -> Location:
        try:
            location = Location(**data.model_dump())
            self.session.add(location)
            await self.session.flush()
            await self.session.refresh(location)
            return location
        except IntegrityError as e:
            raise AlreadyExistsException(
                f"Локация с такими данными уже существует: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании локации: {str(e)}")

    async def update(self, id: int, data: LocationUpdate) -> Optional[Location]:
        try:
            result = await self.session.execute(select(Location).where(Location.id == id))
            location = result.scalar_one_or_none()
            if not location:
                return None

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(location, key, value)

            await self.session.flush()
            await self.session.refresh(location)
            return location
        except IntegrityError as e:
            raise AlreadyExistsException(
                f"Конфликт данных при обновлении локации: {str(e.orig)}"
            )
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении локации: {str(e)}")

    async def delete(self, id: int) -> bool:
        try:
            result = await self.session.execute(select(Location).where(Location.id == id))
            location = result.scalar_one_or_none()
            if not location:
                return False
            await self.session.delete(location)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении локации: {str(e)}")
