from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from pydantic_core import PydanticCustomError  # Импортируем для кастомных 422 ошибок
from typing import Optional

class CommentBase(BaseModel):
    text: str = Field(..., description="Текст комментария")
    image: Optional[str] = None
    author_id: int = Field(..., ge=1)
    post_id: int = Field(..., ge=1)

    @field_validator('post_id', mode='before')
    @classmethod
    def validate_post_id(cls, v):
        if v == 0:
            raise PydanticCustomError(
                'value_error',
                'ID поста не может быть 0. Пожалуйста, выберите существующий пост.'
            )
        return v

    @field_validator('author_id', mode='before')
    @classmethod
    def validate_author_id(cls, v):
        if v == 0:
            raise PydanticCustomError(
                'value_error',
                'ID автора не может быть 0. Пожалуйста, укажите корректного автора.'
            )
        return v

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str):
        if not v.strip():
            raise PydanticCustomError(
                'value_error',
                'Комментарий не может быть пустым или состоять только из пробелов'
            )
        return v


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None

    @field_validator('text')
    @classmethod
    def validate_text_update(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise PydanticCustomError(
                'value_error',
                'Текст комментария не может быть пустым при обновлении'
            )
        return v


class CommentOut(CommentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)