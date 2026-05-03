from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., max_length=256)
    is_published: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None


class LocationOut(LocationBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)