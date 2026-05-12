from fastapi import APIRouter, HTTPException, status
from typing import List

# импортируем репозиторий и схемы
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.locations import LocationCreate, LocationUpdate, LocationOut

router = APIRouter(prefix="/locations", tags=["Locations"])
repo = LocationRepository() # Создаем экземпляр репозитория

@router.get("/", response_model=List[LocationOut])
async def get_all_locations():
    # получаем данные из бд
    return repo.get_all()

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate):
    return repo.create(location_data)

@router.put("/{location_id}", response_model=LocationOut)
async def update_location(location_id: int, location_data: LocationUpdate):
    updated_location = repo.update(location_id, location_data)
    if not updated_location:
        raise HTTPException(status_code=404, detail="Местоположение не найдено")
    return updated_location

@router.delete("/{location_id}")
async def delete_location(location_id: int):
    if not repo.delete(location_id):
        raise HTTPException(status_code=404, detail="Местоположение не найдено")
    return {"detail": f"Местоположение {location_id} успешно удалено"}