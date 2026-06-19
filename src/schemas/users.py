import re
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from pydantic_core import PydanticCustomError  # Защита от 500-х ошибок
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., max_length=150)
    email: EmailStr = Field(..., max_length=254)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str):
        if not v.strip():
            raise PydanticCustomError('value_error', 'Username не может быть пустым')
        if not re.match(r'^[\w.@+-]+$', v):
            raise PydanticCustomError(
                'value_error',
                'Username может содержать только буквы, цифры и символы @/./+/-/_'
            )
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: EmailStr):
        return v.lower()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if v.isdigit() or v.isalpha():
            raise PydanticCustomError(
                'value_error',
                'Пароль должен быть сложнее (содержать и буквы, и цифры)'
            )
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    @field_validator('username', 'email', 'password')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]):
        if v is not None and not str(v).strip():
            raise PydanticCustomError('value_error', 'Поле не может быть пустым при обновлении')
        return v


class UserOut(UserBase):
    id: int
    date_joined: datetime
    is_active: bool
    is_staff: bool

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str