import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print(9, project_root)

# Add the project root to sys.path
if project_root not in sys.path:
    sys.path.append(project_root)
# sys.path.append("/home/ha/Downloads/programs/coding-challenges-main/")
from src.models.base import Base
from src.repositories.quiz_repository import QuizRepository
from src.schemas.quiz import QuizCreate
from src.services.quiz_service import QuizService


@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)
    session = session_local()
    yield session
    session.close()


def test_create_quiz_and_add_participant(db_session):
    quiz_repo = QuizRepository(db_session)
    quiz_service = QuizService(quiz_repo)
    quiz = QuizCreate(quiz_id="23")
    created_quiz = quiz_service.create_quiz(creator_user_id=1, quiz_id=quiz.quiz_id)
    participant = quiz_service.add_participant(created_quiz.quiz_id, user_id=2)
    assert participant.quiz_id == created_quiz.quiz_id
    assert participant.score == 0
