from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic_core import PydanticCustomError
from typing import List, Optional

class PostImageOut(BaseModel):
    id: int
    post_id: int
    image_path: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title: str = Field(..., max_length=256)
    text: str
    image: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: bool = True
    author_id: int = Field(..., ge=1)
    category_id: int = Field(..., ge=1)
    location_id: Optional[int] = Field(default=None, ge=1)

    @field_validator('location_id', mode='before')
    @classmethod
    def zero_to_none(cls, v):
        return None if v == 0 else v

    @field_validator('category_id', mode='before')
    @classmethod
    def validate_category_id(cls, v):
        if v == 0:
            raise PydanticCustomError(
                'value_error',
                'Категория не может быть 0. Пожалуйста, выберите существующую категорию.'
            )
        return v

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str):
        if not v.strip():
            raise PydanticCustomError('value_error', 'Заголовок поста не может быть пустым')
        if len(v) < 3:
            raise PydanticCustomError('value_error', 'Заголовок слишком короткий (минимум 3 символа)')
        return v

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str):
        if not v.strip():
            raise PydanticCustomError('value_error', 'Текст поста не может быть пустым')
        return v


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    image: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    category_id: Optional[int] = Field(None, ge=1)
    location_id: Optional[int] = Field(None, ge=1)

    @field_validator('location_id', mode='before')
    @classmethod
    def zero_to_none(cls, v):
        return None if v == 0 else v

    @field_validator('title', 'text')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise PydanticCustomError('value_error', 'Поле не может быть пустым при обновлении')
        return v

    @field_validator('category_id')
    @classmethod
    def check_category_id(cls, v: int) -> int:
        if v == 0:
            raise PydanticCustomError(
                'value_error',
                'Категория не может быть 0. Пожалуйста, выберите существующую категорию.'
            )
        return v


class PostOut(PostBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)