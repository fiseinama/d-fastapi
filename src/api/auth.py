from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm  # <-- Импортируем форму
from src.domain.use_cases.auth import AuthUseCase
from src.schemas.users import Token

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_use_case = AuthUseCase()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    token_data = auth_use_case.login_user(
        username=form_data.username, # form_data автоматически достает username и password из swagger
        password=form_data.password
    )
    return token_data