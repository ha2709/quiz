from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Participant, Question, QuizSession
from src.schemas.question import QuestionCreate
from src.schemas.quiz import QuizCreate


class QuizRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_quiz(self, quiz_id: str, creator_id: int) -> QuizSession:
        quiz = QuizSession(quiz_id=quiz_id, creator_user_id=creator_id, status="active")
        print(17, quiz.creator_user_id)
        self.db.add(quiz)
        await self.db.commit()
        await self.db.refresh(quiz)
        return quiz

    async def add_participant(self, quiz_id: str, user_id: int) -> Participant:
        result = await self.db.execute(
            select(Participant).filter_by(quiz_id=quiz_id, user_id=user_id)
        )
        participant = result.scalars().first()
        if not participant:
            participant = Participant(quiz_id=quiz_id, user_id=user_id, score=0)
            self.db.add(participant)
            await self.db.commit()
            await self.db.refresh(participant)
        return participant

    async def update_score(
        self, quiz_id: str, user_id: int, increment: int = 10
    ) -> int:
        result = await self.db.execute(
            select(Participant).filter_by(quiz_id=quiz_id, user_id=user_id)
        )
        participant = result.scalars().first()
        if participant:
            participant.score += increment
            await self.db.commit()
            return participant.score
        return 0

    async def get_leaderboard(self, quiz_id: str) -> List[dict]:
        result = await self.db.execute(
            select(Participant)
            .filter_by(quiz_id=quiz_id)
            .order_by(Participant.score.desc())
        )
        participants = result.scalars().all()
        # print(55, participants)
        return [{"username": p.user.username, "score": p.score} for p in participants]

    async def add_question(self, quiz_id: str, question_in: QuestionCreate) -> Question:
        question = Question(
            quiz_id=quiz_id,
            text=question_in.text,
            options=question_in.options,
            correct_option=question_in.correct_option,
        )
        self.db.add(question)
        await self.db.commit()
        await self.db.refresh(question)
        return question

    async def get_questions(self, quiz_id: str) -> List[Question]:
        result = await self.db.execute(select(Question).filter_by(quiz_id=quiz_id))
        return result.scalars().all()

    async def get_quiz_by_id(self, quiz_id: str) -> QuizSession:
        result = await self.db.execute(select(QuizSession).filter_by(quiz_id=quiz_id))
        return result.scalars().first()

    async def get_participants(self, quiz_id: str) -> List[Participant]:
        result = await self.db.execute(select(Participant).filter_by(quiz_id=quiz_id))
        return result.scalars().all()
