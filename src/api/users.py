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