from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    username: str
    score: int

    class Config:
        orm_mode = True


class Leaderboard(BaseModel):
    quiz_id: str
    entries: list[LeaderboardEntry]
