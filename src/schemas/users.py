from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., max_length=150)
    email: str = Field(..., max_length=254)

class UserCreate(UserBase):
    password: str = Field(..., max_length=128)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    date_joined: datetime
    is_active: bool
    is_staff: bool

    model_config = ConfigDict(from_attributes=True)