from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(String, ForeignKey("quiz_sessions.quiz_id"), nullable=False)
    text = Column(String, nullable=False)
    options = Column(String, nullable=False)  # Store as JSON string
    correct_option = Column(Integer, nullable=False)

    quiz_session = relationship("QuizSession", back_populates="questions")
