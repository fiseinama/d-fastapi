from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic_core import PydanticCustomError  # Спасает от 500-й ошибки
from typing import Optional

class CategoryBase(BaseModel):
    title: str = Field(..., max_length=256)
    description: Optional[str] = None
    slug: str = Field(..., max_length=64, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: bool = True

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str):
        if not v.strip():
            raise PydanticCustomError(
                'value_error',
                'Заголовок категории не может быть пустым или состоять только из пробелов'
            )
        return v

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str):
        if not v.strip():
            raise PydanticCustomError('value_error', 'Slug не может быть пустым')
        if v.startswith('-') or v.endswith('-'):
            raise PydanticCustomError('value_error', 'Slug не может начинаться или заканчиваться дефисом')
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(None, max_length=64, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise PydanticCustomError('value_error', 'Обновленный заголовок не может быть пустым')
        return v

    # Добавили проверку slug при обновлении, чтобы защитить базу данных
    @field_validator('slug')
    @classmethod
    def validate_slug_update(cls, v: Optional[str]):
        if v is not None:
            if not v.strip():
                raise PydanticCustomError('value_error', 'Обновленный slug не может быть пустым')
            if v.startswith('-') or v.endswith('-'):
                raise PydanticCustomError('value_error', 'Обновленный slug не может начинаться или заканчиваться дефисом')
        return v


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)