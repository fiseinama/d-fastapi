from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., max_length=256)
    text: str
    pub_date: Optional[datetime] = None
    is_published: bool = True
    author_id: int = Field(..., ge=1)
    category_id: int = Field(..., ge=1)
    location_id: Optional[int] = Field(default=None, ge=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    category_id: Optional[int] = Field(None, ge=1)
    location_id: Optional[int] = Field(None, ge=1)


class PostOut(PostBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)