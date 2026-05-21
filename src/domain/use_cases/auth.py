from src.infrastructure.sqlite.repositories.user import UserRepository
from src.core.security import verify_password, create_access_token
from src.core.exceptions import UnauthorizedException


class AuthUseCase:
    def __init__(self):
        self.user_repo = UserRepository()

    def login_user(self, username: str, password: str) -> dict:
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UnauthorizedException("Неверное имя пользователя или пароль")

        if not verify_password(password, user.password):
            raise UnauthorizedException("Неверное имя пользователя или пароль")

        access_token = create_access_token(data={"sub": str(user.id), "username": user.username})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }