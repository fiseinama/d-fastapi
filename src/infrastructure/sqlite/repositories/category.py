from typing import List, Optional
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.category import Category
from src.schemas.categories import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def get_all(self) -> List[Category]:
        with get_session() as session:
            return session.query(Category).all()

    def get_by_id(self, id: int) -> Optional[Category]:
        with get_session() as session:
            return session.query(Category).filter(Category.id == id).first()

    def create(self, data: CategoryCreate) -> Category:
        with get_session() as session:
            category = Category(**data.model_dump())
            session.add(category)
            return category

    def update(self, id: int, data: CategoryUpdate) -> Optional[Category]:
        with get_session() as session:
            category = session.query(Category).filter(Category.id == id).first()
            if not category:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(category, key, value)
            return category

    def delete(self, id: int) -> bool:
        with get_session() as session:
            category = session.query(Category).filter(Category.id == id).first()
            if not category:
                return False
            session.delete(category)
            return True