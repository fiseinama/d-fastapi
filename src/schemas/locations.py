from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic_core import PydanticCustomError  # Наш щит от 500-х ошибок
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., max_length=256)
    is_published: bool = True

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str):
        if not v.strip():
            raise PydanticCustomError('value_error', 'Название локации не может быть пустым')
        if len(v.strip()) < 2:
            raise PydanticCustomError('value_error', 'Название локации слишком короткое')
        return v


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None

    @field_validator('name')
    @classmethod
    def validate_name_update(cls, v: Optional[str]):
        if v is not None:
            if not v.strip():
                raise PydanticCustomError('value_error', 'При обновлении название не может быть пустым')
            if len(v.strip()) < 2:
                raise PydanticCustomError('value_error', 'Обновленное название слишком короткое')
        return v


class LocationOut(LocationBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)