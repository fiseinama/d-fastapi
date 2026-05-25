from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from src.schemas.users import UserCreate, UserOut, UserUpdate
from src.domain.use_cases.users import UserUseCase
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
use_case = UserUseCase()

@router.get("/", response_model=List[UserOut])
async def get_all_users(current_user: str = Depends(get_current_user)):
    print(f"Список пользователей запросил: {current_user}")
    return use_case.get_all()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    return use_case.create_user(user_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
        user_id: int,
        user_data: UserUpdate,
        current_user=Depends(get_current_user)  # <-- Требуем токен
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете редактировать только свой собственный профиль!"
        )

    print(f"Пользователь {current_user.username} обновляет свой профиль")
    return use_case.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете удалить только свой собственный профиль!"
        )

    print(f"Пользователь {current_user.username} удаляет свой аккаунт")
    use_case.delete_user(user_id)
    return None