from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(String, ForeignKey("quiz_sessions.quiz_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)

    user = relationship("User", back_populates="participant_quizzes")
    quiz_session = relationship("QuizSession", back_populates="participants")
