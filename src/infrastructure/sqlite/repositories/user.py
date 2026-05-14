from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.users import User
from src.schemas.users import UserCreate, UserUpdate
from src.core.exceptions import AlreadyExistsException, InfrastructureException

class UserRepository:

    def get_all(self) -> List[User]:
        try:
            with get_session() as session:
                users = session.query(User).all()
                session.expunge_all()
                return users
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении списка пользователей: {str(e)}")

    def get_by_id(self, id: int) -> Optional[User]:
        try:
            with get_session() as session:
                user = session.query(User).filter(User.id == id).first()
                if user:
                    session.expunge(user) # Отвязываем конкретный объект
                return user
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при поиске пользователя по ID: {str(e)}")

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            with get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                if user:
                    session.expunge(user)
                return user
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при поиске пользователя по имени: {str(e)}")

    def create(self, data: UserCreate) -> User:
        try:
            with get_session() as session:
                user = User(**data.model_dump())
                session.add(user)
                session.commit()
                session.refresh(user)
                session.expunge(user)
                return user
        except IntegrityError as e:
            raise AlreadyExistsException(f"Пользователь с таким именем или email уже существует")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании пользователя: {str(e)}")

    def update(self, id: int, data: UserUpdate) -> Optional[User]:
        try:
            with get_session() as session:
                user = session.query(User).filter(User.id == id).first()
                if not user:
                    return None

                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(user, key, value)

                session.commit()
                session.refresh(user)
                session.expunge(user)
                return user
        except IntegrityError as e:
            raise AlreadyExistsException(f"Конфликт данных при обновлении")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении пользователя: {str(e)}")

    def delete(self, id: int) -> bool:
        try:
            with get_session() as session:
                user = session.query(User).filter(User.id == id).first()
                if not user:
                    return False
                session.delete(user)
                session.commit()
                return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении пользователя: {str(e)}")