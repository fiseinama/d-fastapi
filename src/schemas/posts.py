from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., max_length=256)
    text: str
    pub_date: Optional[datetime] = None
    is_published: bool = True
    author_id: int = Field(..., ge=1)
    category_id: int = Field(..., ge=1)
    location_id: Optional[int] = Field(default=None, ge=1)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str):
        if not v.strip():
            raise ValueError('Заголовок поста не может быть пустым')
        if len(v) < 3:
            raise ValueError('Заголовок слишком короткий (минимум 3 символа)')
        return v

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str):
        if not v.strip():
            raise ValueError('Текст поста не может быть пустым')
        return v


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    category_id: Optional[int] = Field(None, ge=1)
    location_id: Optional[int] = Field(None, ge=1)

    @field_validator('title', 'text')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError('Поле не может быть пустым при обновлении')
        return v


class PostOut(PostBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)