from typing import Literal

from pydantic import BaseModel, EmailStr

Role = Literal["viewer", "analyst", "admin"]


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Role = "viewer"


class UserUpdate(BaseModel):
    role: Role | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    id: int
    role: Role
    is_active: bool

    class Config:
        orm_mode = True
