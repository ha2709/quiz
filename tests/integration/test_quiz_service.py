import os
import random
import sys

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Determine the project root (two directories up)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Add the project root to sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

print(9, project_root)
# put import here to update the project folder for import

from src.models.base import Base
from src.repositories.quiz_repository import QuizRepository
from src.schemas.quiz import QuizCreate
from src.services.quiz_service import QuizService


@pytest.fixture(scope="module")
async def async_db_session():
    # Create an asynchronous engine using aiosqlite for in-memory SQLite
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a configured "Session" class
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create a session
    async with async_session() as session:
        yield session  # Provide the session to the test
        await session.rollback()  # Rollback any changes after the test

    # Dispose the engine after tests
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_quiz_and_add_participant(async_db_session: AsyncSession):
    # Initialize repositories and services with the async session
    quiz_repo = QuizRepository(async_db_session)
    quiz_service = QuizService(quiz_repo)

    # Generate a random quiz_id
    random_quiz_id = str(random.randint(10000, 99999))
    quiz_id = random_quiz_id
    print(40, quiz_id)

    # Call the asynchronous create_quiz method and await its completion
    created_quiz = await quiz_service.create_quiz(creator_id=1, quiz_id=quiz_id)

    # Call the asynchronous add_participant method and await its completion
    participant = await quiz_service.add_participant(created_quiz.quiz_id, user_id=2)

    # Assertions to verify the participant was added correctly
    assert participant.quiz_id == created_quiz.quiz_id
    assert participant.score == 0
