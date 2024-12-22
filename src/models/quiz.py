import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    quiz_id = Column(String, primary_key=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="active")  # active, started, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    creator = relationship("User", back_populates="quizzes_created")
    participants = relationship("Participant", back_populates="quiz_session")
    questions = relationship("Question", back_populates="quiz_session")

    __table_args__ = (
        Index("idx_creator_user_id_status", "creator_user_id", "status"),
        Index("idx_quiz_created_at", "created_at"),
    )
