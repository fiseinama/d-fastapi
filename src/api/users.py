from fastapi import APIRouter, status
from typing import List
from src.schemas.users import UserCreate, UserOut, UserUpdate
from src.domain.use_cases.users import UserUseCase

router = APIRouter(prefix="/users", tags=["Users"])
use_case = UserUseCase()

@router.get("/", response_model=List[UserOut])
async def get_all_users():
    return use_case.get_all()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    return use_case.create_user(user_data)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserUpdate):
    return use_case.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    use_case.delete_user(user_id)
    return None