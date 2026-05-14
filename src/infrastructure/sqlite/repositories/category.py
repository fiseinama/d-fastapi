from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryCreate, CategoryUpdate
from src.core.exceptions import AlreadyExistsException, InfrastructureException

class CategoryRepository:
    def get_all(self) -> List[Category]:
        try:
            with get_session() as session:
                return session.query(Category).all()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении категорий: {str(e)}")

    def get_by_id(self, id: int) -> Optional[Category]:
        try:
            with get_session() as session:
                return session.query(Category).filter(Category.id == id).first()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении категории: {str(e)}")

    def create(self, data: CategoryCreate) -> Category:
        try:
            with get_session() as session:
                category = Category(**data.model_dump())
                session.add(category)
                session.commit()
                session.refresh(category)
                return category
        except IntegrityError as e:
            raise AlreadyExistsException(f"Категория с такими данными уже существует: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании категории: {str(e)}")

    def update(self, id: int, data: CategoryUpdate) -> Optional[Category]:
        try:
            with get_session() as session:
                category = session.query(Category).filter(Category.id == id).first()
                if not category:
                    return None
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(category, key, value)
                session.commit()
                session.refresh(category)
                return category
        except IntegrityError as e:
            raise AlreadyExistsException(f"Ошибка обновления: данные уже заняты: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении категории: {str(e)}")

    def delete(self, id: int) -> bool:
        try:
            with get_session() as session:
                category = session.query(Category).filter(Category.id == id).first()
                if not category:
                    return False
                session.delete(category)
                session.commit()
                return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении категории: {str(e)}")