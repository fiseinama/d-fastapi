from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationCreate, LocationUpdate
# Исправь импорт в соответствии с путем к твоему файлу исключений
from src.core.exceptions import AlreadyExistsException, InfrastructureException


class LocationRepository:
    def get_all(self) -> List[Location]:
        try:
            with get_session() as session:
                return session.query(Location).all()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении локаций: {str(e)}")

    def get_by_id(self, id: int) -> Optional[Location]:
        try:
            with get_session() as session:
                return session.query(Location).filter(Location.id == id).first()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении локации: {str(e)}")

    def create(self, data: LocationCreate) -> Location:
        try:
            with get_session() as session:
                location = Location(**data.model_dump())
                session.add(location)
                session.commit()
                session.refresh(location)
                return location
        except IntegrityError as e:
            raise AlreadyExistsException(f"Локация с такими данными уже существует: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании локации: {str(e)}")

    def update(self, id: int, data: LocationUpdate) -> Optional[Location]:
        try:
            with get_session() as session:
                location = session.query(Location).filter(Location.id == id).first()
                if not location:
                    return None

                update_data = data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(location, key, value)

                session.commit()
                session.refresh(location)
                return location
        except IntegrityError as e:
            raise AlreadyExistsException(f"Конфликт данных при обновлении локации: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении локации: {str(e)}")

    def delete(self, id: int) -> bool:
        try:
            with get_session() as session:
                location = session.query(Location).filter(Location.id == id).first()
                if not location:
                    return False
                session.delete(location)
                session.commit()
                return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении локации: {str(e)}")