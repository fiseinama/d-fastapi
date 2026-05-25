from fastapi import APIRouter, status, Depends
from typing import List
from src.schemas.locations import LocationCreate, LocationUpdate, LocationOut
from src.domain.use_cases.locations import LocationUseCase
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/locations", tags=["Locations"])
use_case = LocationUseCase()

@router.get("/", response_model=List[LocationOut])
async def get_all_locations():
    return use_case.get_all()

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    current_user = Depends(get_current_user)
):
    return use_case.create_location(location_data)

@router.put("/{location_id}", response_model=LocationOut)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    current_user = Depends(get_current_user)
):
    return use_case.update_location(location_id, location_data)

@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    current_user = Depends(get_current_user)
):
    use_case.delete_location(location_id)
    return {"detail": f"Местоположение {location_id} успешно удалено"}