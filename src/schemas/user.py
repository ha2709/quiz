from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password_hash: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
