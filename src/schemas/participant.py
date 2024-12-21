from pydantic import BaseModel


class ParticipantRead(BaseModel):
    id: int
    quiz_id: str
    user_id: int
    score: int

    class Config:
        orm_mode = True
