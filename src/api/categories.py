from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from src.schemas.categories import CategoryCreate, CategoryUpdate, CategoryOut
from src.domain.use_cases.categories import CategoryUseCase
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])
use_case = CategoryUseCase()

@router.get("/", response_model=List[CategoryOut])
async def get_all_categories():
    return use_case.get_all()

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user = Depends(get_current_user)
):
    return use_case.create_category(category_data)

@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user = Depends(get_current_user)
):
    return use_case.update_category(category_id, data=category_data)

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user = Depends(get_current_user)
):
    use_case.delete_category(category_id)
    return {"detail": f"Категория {category_id} успешно удалена"}