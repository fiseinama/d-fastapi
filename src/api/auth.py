from fastapi import APIRouter, Depends
from src.schemas.users import UserLogin, Token
from src.domain.use_cases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    auth_use_case = AuthUseCase()
    return auth_use_case.login_user(login_data.username, login_data.password)