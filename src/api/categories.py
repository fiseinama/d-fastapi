from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from src.schemas.categories import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])

db_categories: List[CategoryOut] = []


@router.get("/", response_model=List[CategoryOut])
async def get_all_categories():
    return db_categories


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    new_id = len(db_categories) + 1
    new_category = CategoryOut(
        id=new_id,
        created_at=datetime.now(),
        **category_data.model_dump()
    )
    db_categories.append(new_category)
    return new_category


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category_data: CategoryUpdate):
    for index, cat in enumerate(db_categories):
        if cat.id == category_id:
            update_dict = category_data.model_dump(exclude_unset=True)
            updated_data = cat.model_dump()
            updated_data.update(update_dict)
            db_categories[index] = CategoryOut(**updated_data)
            return db_categories[index]
    raise HTTPException(status_code=404, detail="Категория не найдена")


@router.delete("/{category_id}")
async def delete_category(category_id: int):
    for index, cat in enumerate(db_categories):
        if cat.id == category_id:
            db_categories.pop(index)
            return {"detail": f"Категория {category_id} успешно удалена"}
    raise HTTPException(status_code=404, detail="Категория не найдена")