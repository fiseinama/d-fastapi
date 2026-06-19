from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationCreate, LocationUpdate


class LocationUseCase:
    def __init__(self, session: AsyncSession):
        self.repo = LocationRepository(session)

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, location_id: int):
        location = await self.repo.get_by_id(location_id)
        if not location:
            raise NotFoundException(f"Локация с ID {location_id} не найдена")
        return location

    async def create_location(self, data: LocationCreate):
        try:
            return await self.repo.create(data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать локацию '{data.name}': {e.message}")

    async def update_location(self, location_id: int, data: LocationUpdate):
        location = await self.repo.update(location_id, data)
        if not location:
            raise NotFoundException(f"Локация с ID {location_id} не найдена")
        return location

    async def delete_location(self, location_id: int):
        if not await self.repo.delete(location_id):
            raise NotFoundException(f"Локация с ID {location_id} не найдена для удаления")
        return True
