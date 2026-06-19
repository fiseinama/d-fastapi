from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db, get_current_user
from src.domain.use_cases.locations import LocationUseCase
from src.schemas.locations import LocationCreate, LocationOut, LocationUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])


def get_location_use_case(db: AsyncSession = Depends(get_db)) -> LocationUseCase:
    return LocationUseCase(db)


@router.get("/", response_model=List[LocationOut])
async def get_all_locations(use_case: LocationUseCase = Depends(get_location_use_case)):
    return await use_case.get_all()


@router.get("/{location_id}", response_model=LocationOut)
async def get_location(
    location_id: int,
    use_case: LocationUseCase = Depends(get_location_use_case),
):
    return await use_case.get_by_id(location_id)


@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    current_user=Depends(get_current_user), # <-- Заменено на обычного юзера
    use_case: LocationUseCase = Depends(get_location_use_case),
):
    return await use_case.create_location(location_data)


@router.put("/{location_id}", response_model=LocationOut)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    current_user=Depends(get_current_user), # <-- Заменено на обычного юзера
    use_case: LocationUseCase = Depends(get_location_use_case),
):
    return await use_case.update_location(location_id, location_data)


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    current_user=Depends(get_current_user), # <-- Заменено на обычного юзера
    use_case: LocationUseCase = Depends(get_location_use_case),
):
    await use_case.delete_location(location_id)
    return {"detail": f"Местоположение {location_id} успешно удалено"}