import re
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional

class UserBase(BaseModel):
    # Используем EmailStr для автоматической проверки формата почты
    username: str = Field(..., max_length=150)
    email: str = Field(..., max_length=254)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str):
        if not re.match(r'^[\w.@+-]+$', v):
            raise ValueError(
                'Username может содержать только буквы, цифры и символы @/./+/-/_'
            )
        if not v.strip():
            raise ValueError('Username не может быть пустым')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str):
        if "@" not in v or "." not in v:
            raise ValueError('Некорректный формат email')
        return v.lower()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if v.isdigit() or v.isalpha():
            raise ValueError('Пароль должен быть сложнее (содержать и буквы, и цифры)')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=150)
    email: Optional[str] = Field(None, max_length=254)
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    @field_validator('username', 'email', 'password')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError('Поле не может быть пустым при обновлении')
        return v


class UserOut(UserBase):
    id: int
    date_joined: datetime
    is_active: bool
    is_staff: bool

    model_config = ConfigDict(from_attributes=True)

# Схема, которую пришлет пользователь при логине
class UserLogin(BaseModel):
    username: str
    password: str

# Схема, которую мы вернем в ответ на успешный логин
class Token(BaseModel):
    access_token: str
    token_type: str