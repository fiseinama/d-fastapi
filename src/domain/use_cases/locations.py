from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.schemas.locations import LocationCreate, LocationUpdate

class LocationUseCase:
    def __init__(self):
        self.repo = LocationRepository()

    def get_all(self):
        return self.repo.get_all()

    def create_location(self, data: LocationCreate):
        try:
            return self.repo.create(data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать локацию '{data.name}': {e.message}")

    def update_location(self, location_id: int, data: LocationUpdate):
        location = self.repo.update(location_id, data)
        if not location:
            raise NotFoundException(f"Локация с ID {location_id} не найдена")
        return location

    def delete_location(self, location_id: int):
        if not self.repo.delete(location_id):
            raise NotFoundException(f"Локация с ID {location_id} не найдена для удаления")
        return True