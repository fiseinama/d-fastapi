from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.users import UserCreate, UserOut, UserUpdate
from src.infrastructure.sqlite.repositories.user import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])
repo = UserRepository()

@router.get("/", response_model=List[UserOut])
async def get_all_users():
    return repo.get_all()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    if repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return repo.create(user_data)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserUpdate):
    updated_user = repo.update(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    success = repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return None