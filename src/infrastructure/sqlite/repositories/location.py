from typing import List, Optional
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.location import Location
from src.schemas.locations import LocationCreate, LocationUpdate


class LocationRepository:
    def get_all(self) -> List[Location]:
        with get_session() as session:
            return session.query(Location).all()

    def get_by_id(self, id: int) -> Optional[Location]:
        with get_session() as session:
            return session.query(Location).filter(Location.id == id).first()

    def create(self, data: LocationCreate) -> Location:
        with get_session() as session:
            location = Location(**data.model_dump())
            session.add(location)
            return location

    def update(self, id: int, data: LocationUpdate) -> Optional[Location]:
        with get_session() as session:
            location = session.query(Location).filter(Location.id == id).first()
            if not location:
                return None

            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(location, key, value)

            return location

    def delete(self, id: int) -> bool:
        with get_session() as session:
            location = session.query(Location).filter(Location.id == id).first()
            if not location:
                return False
            session.delete(location)
            return True