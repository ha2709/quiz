from pydantic import BaseModel


class QuestionCreate(BaseModel):
    text: str
    options: str
    correct_option: int


class QuestionRead(BaseModel):
    id: int
    text: str
    options: str
    correct_option: int

    class Config:
        orm_mode = True
