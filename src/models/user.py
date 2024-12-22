import datetime

from sqlalchemy import Column, DateTime, Index, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String(), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    quizzes_created = relationship("QuizSession", back_populates="creator")
    participant_quizzes = relationship("Participant", back_populates="user")

    __table_args__ = (Index("idx_username_created_at", "username", "created_at"),)
