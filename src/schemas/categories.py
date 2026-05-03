from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    title: str = Field(..., max_length=256)
    description: Optional[str] = None
    slug: str = Field(..., max_length=64, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(None, max_length=64)
    is_published: Optional[bool] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)