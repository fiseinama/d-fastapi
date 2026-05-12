from typing import List, Optional
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.users import User
from src.schemas.users import UserCreate, UserUpdate, UserOut


class UserRepository:

    def get_all(self) -> List[User]:
        with get_session() as session:
            return session.query(User).all()

    def get_by_id(self, id: int) -> Optional[User]:
        with get_session() as session:
            return session.query(User).filter(User.id == id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        with get_session() as session:
            return session.query(User).filter(User.username == username).first()

    def create(self, data: UserCreate) -> User:
        with get_session() as session:
            user = User(**data.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def update(self, id: int, data: UserUpdate) -> Optional[User]:
        with get_session() as session:
            user = self.get_by_id(id)
            if not user:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            session.commit()
            session.refresh(user)
            return user

    def delete(self, id: int) -> bool:
        with get_session() as session:
            user = self.get_by_id(id)
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True