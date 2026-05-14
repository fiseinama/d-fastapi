from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

class CommentBase(BaseModel):
    text: str = Field(..., description="Текст комментария")
    author_id: int = Field(..., ge=1)
    post_id: int = Field(..., ge=1)

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str):
        if not v.strip():
            raise ValueError('Комментарий не может быть пустым или состоять только из пробелов')
        return v


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[str] = None

    @field_validator('text')
    @classmethod
    def validate_text_update(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError('Текст комментария не может быть пустым при обновлении')
        return v


class CommentOut(CommentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)