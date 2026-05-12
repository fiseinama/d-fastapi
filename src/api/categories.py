from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.categories import CategoryCreate, CategoryUpdate, CategoryOut
from src.infrastructure.sqlite.repositories.category import CategoryRepository

router = APIRouter(prefix="/categories", tags=["Categories"])
repo = CategoryRepository()

@router.get("/", response_model=List[CategoryOut])
async def get_all_categories():
    return repo.get_all()

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    try:
        return repo.create(category_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category_data: CategoryUpdate):
    category = repo.update(category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    if not repo.delete(category_id):
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return {"detail": f"Категория {category_id} успешно удалена"}