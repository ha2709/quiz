from typing import List

from src.models import Participant, Question, QuizSession
from src.repositories.quiz_repository import QuizRepository
from src.schemas.question import QuestionCreate
from src.schemas.quiz import QuizCreate, QuizRead
from src.utils.exceptions import QuizNotFoundException


class QuizService:
    def __init__(self, quiz_repository: QuizRepository):
        self.quiz_repository = quiz_repository

    async def create_quiz(self, quiz_in: QuizCreate, creator_id: int) -> QuizSession:
        return await self.quiz_repository.create_quiz(quiz_in, creator_id)

    async def get_quiz(self, quiz_id: str) -> QuizSession:
        quiz = await self.quiz_repository.get_quiz_by_id(quiz_id)
        if not quiz:
            raise QuizNotFoundException(detail=f"Quiz {quiz_id} not found.")
        return quiz

    async def add_participant(self, quiz_id: str, user_id: int) -> Participant:
        await self.get_quiz(quiz_id)  # Ensure quiz exists
        return await self.quiz_repository.add_participant(quiz_id, user_id)

    async def update_score(
        self, quiz_id: str, user_id: int, increment: int = 10
    ) -> int:
        await self.get_quiz(quiz_id)  # Ensure quiz exists
        return await self.quiz_repository.update_score(quiz_id, user_id, increment)

    async def get_leaderboard(self, quiz_id: str) -> List[dict]:
        await self.get_quiz(quiz_id)  # Ensure quiz exists
        return await self.quiz_repository.get_leaderboard(quiz_id)

    async def add_question(self, quiz_id: str, question_in: QuestionCreate) -> Question:
        await self.get_quiz(quiz_id)  # Ensure quiz exists
        return await self.quiz_repository.add_question(quiz_id, question_in)

    async def get_questions(self, quiz_id: str) -> List[Question]:
        await self.get_quiz(quiz_id)  # Ensure quiz exists

    async def get_participants(self, quiz_id: str) -> List[Participant]:
        return await self.quiz_repository.get_participants(quiz_id)
