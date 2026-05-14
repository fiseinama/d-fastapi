from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., max_length=256)
    is_published: bool = True

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str):
        # Проверяем на пустоту и минимальную длину осмысленного текста
        if not v.strip():
            raise ValueError('Название локации не может быть пустым')
        if len(v.strip()) < 2:
            raise ValueError('Название локации слишком короткое')
        return v


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None

    @field_validator('name')
    @classmethod
    def validate_name_update(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError('При обновлении название не может быть пустым')
        return v


class LocationOut(LocationBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)