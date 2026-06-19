from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user, get_db
from src.domain.use_cases.users import UserUseCase
from src.infrastructure.sqlite.models.users import User
from src.schemas.users import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_use_case(db: AsyncSession = Depends(get_db)) -> UserUseCase:
    return UserUseCase(db)


@router.get("/", response_model=List[UserOut])
async def get_all_users(
    current_user: User = Depends(get_current_user),
    use_case: UserUseCase = Depends(get_user_use_case),
):
    return await use_case.get_all()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    use_case: UserUseCase = Depends(get_user_use_case),
    current_user: User = Depends(get_current_user),
):
    return await use_case.get_by_id(user_id)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: UserUseCase = Depends(get_user_use_case),
):
    return await use_case.create_user(user_data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user=Depends(get_current_user),
    use_case: UserUseCase = Depends(get_user_use_case),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете редактировать только свой собственный профиль!",
        )

    return await use_case.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user=Depends(get_current_user),
    use_case: UserUseCase = Depends(get_user_use_case),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете удалить только свой собственный профиль!",
        )

    await use_case.delete_user(user_id)
    return None
