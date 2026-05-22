from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer  # <-- Меняем импорт здесь
from src.core.security import decode_access_token
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.core.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme)
):
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Невалидный токен")

    user_repo = UserRepository()
    user = user_repo.get_by_id(int(user_id))
    if user is None:
        raise UnauthorizedException("Пользователь не найден")

    return user