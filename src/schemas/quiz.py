from typing import Optional

from pydantic import BaseModel


class QuizCreate(BaseModel):
    quiz_id: str = None  # Optional, will be auto-generated if not provided


class QuizRead(BaseModel):
    quiz_id: str
    creator_user_id: int
    status: str

    class Config:
        orm_mode = True
