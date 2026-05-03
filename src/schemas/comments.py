from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CommentBase(BaseModel):
    text: str
    author_id: int = Field(..., ge=1)
    post_id: int = Field(..., ge=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[str] = None


class CommentOut(CommentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)