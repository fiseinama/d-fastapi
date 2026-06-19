from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UnauthorizedException
from src.core.logger import logger
from src.core.security import create_access_token, verify_password
from src.infrastructure.sqlite.repositories.user import UserRepository


class AuthUseCase:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def login_user(self, username: str, password: str) -> dict:
        user = await self.user_repo.get_by_username(username)
        if not user:
            logger.warning(f"Неудачная попытка входа: пользователь '{username}' не найден")
            raise UnauthorizedException("Неверное имя пользователя или пароль")

        if not verify_password(password, user.password):
            logger.warning(f"Неудачная попытка входа: неверный пароль для пользователя '{username}'")
            raise UnauthorizedException("Неверное имя пользователя или пароль")

        access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
        logger.info(f"Пользователь '{username}' (ID: {user.id}) успешно авторизован")

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
