from pydantic import BaseModel


class ParticipantRead(BaseModel):
    user_id: int
    score: int

    class Config:
        orm_mode = True
