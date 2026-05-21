from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.security import decode_access_token
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.core.exceptions import UnauthorizedException

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Невалидный токен")

    user_repo = UserRepository()
    user = user_repo.get_by_id(int(user_id))
    if user is None:
        raise UnauthorizedException("Пользователь не найден")

    return user