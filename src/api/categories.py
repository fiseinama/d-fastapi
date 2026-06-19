from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db, get_current_user
from src.domain.use_cases.categories import CategoryUseCase
from src.schemas.categories import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_use_case(db: AsyncSession = Depends(get_db)) -> CategoryUseCase:
    return CategoryUseCase(db)


@router.get("/", response_model=List[CategoryOut])
async def get_all_categories(use_case: CategoryUseCase = Depends(get_category_use_case)):
    return await use_case.get_all()


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: int,
    use_case: CategoryUseCase = Depends(get_category_use_case),
):
    return await use_case.get_by_id(category_id)


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user=Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case),
):
    return await use_case.create_category(category_data)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user=Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case),
):
    return await use_case.update_category(category_id, data=category_data)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user=Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case),
):
    await use_case.delete_category(category_id)
    return {"detail": f"Категория {category_id} успешно удалена"}