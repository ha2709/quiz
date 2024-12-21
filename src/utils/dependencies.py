from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import AsyncSessionLocal
from src.repositories.quiz_repository import QuizRepository
from src.repositories.user_repository import UserRepository
from src.services.quiz_service import QuizService
from src.services.user_service import UserService


# Dependency to provide an AsyncSession
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# Async-compatible QuizService provider
async def get_quiz_service(db: AsyncSession = Depends(get_db)) -> QuizService:
    quiz_repository = QuizRepository(db)
    return QuizService(quiz_repository)


# Async-compatible UserService provider
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)
