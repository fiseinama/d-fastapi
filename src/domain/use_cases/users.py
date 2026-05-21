from src.infrastructure.sqlite.repositories.user import UserRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.schemas.users import UserCreate, UserUpdate

from src.core.security import hash_password


class UserUseCase:
    def __init__(self):
        self.repo = UserRepository()

    def get_all(self):
        return self.repo.get_all()

    def create_user(self, data: UserCreate):
        if self.repo.get_by_username(data.username):
            raise AlreadyExistsException(f"Пользователь '{data.username}' уже зарегистрирован")

        try:

            data.password = hash_password(data.password)

            return self.repo.create(data)

        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать аккаунт: {e.message}")

    def update_user(self, user_id: int, data: UserUpdate):
        user = self.repo.update(user_id, data)
        if not user:
            raise NotFoundException(f"Пользователь с ID {user_id} не найден")
        return user

    def delete_user(self, user_id: int):
        if not self.repo.delete(user_id):
            raise NotFoundException(f"Не удалось удалить: пользователь {user_id} не найден")
        return True