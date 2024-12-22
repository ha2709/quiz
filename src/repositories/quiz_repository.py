from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Participant, Question, QuizSession
from src.schemas.question import QuestionCreate
from src.utils.logger import LoggerSingleton


class QuizRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = LoggerSingleton().logger

    async def create_quiz(self, quiz_id: str, creator_id: int) -> QuizSession:
        self.logger.info(
            f"Creating quiz with ID: {quiz_id} for creator ID: {creator_id}"
        )
        try:
            quiz = QuizSession(
                quiz_id=quiz_id, creator_user_id=creator_id, status="active"
            )
            self.db.add(quiz)
            await self.db.commit()
            await self.db.refresh(quiz)
            self.logger.info(f"Quiz created successfully with ID: {quiz.quiz_id}")
            return quiz
        except Exception as e:
            self.logger.error(f"Error creating quiz with ID {quiz_id}: {str(e)}")
            raise e

    async def add_participant(self, quiz_id: str, user_id: int) -> Participant:
        self.logger.info(
            f"Adding participant with user ID: {user_id} to quiz ID: {quiz_id}"
        )
        try:
            result = await self.db.execute(
                select(Participant).filter_by(quiz_id=quiz_id, user_id=user_id)
            )
            participant = result.scalars().first()
            if not participant:
                self.logger.debug(f"Creating new participant for quiz ID: {quiz_id}")
                participant = Participant(quiz_id=quiz_id, user_id=user_id, score=0)
                self.db.add(participant)
                await self.db.commit()
                await self.db.refresh(participant)
            self.logger.info(
                f"Participant added successfully with ID: {participant.id}"
            )
            return participant
        except Exception as e:
            self.logger.error(
                f"Error adding participant to quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def update_score(
        self, quiz_id: str, user_id: int, increment: int = 10
    ) -> int:
        self.logger.info(f"Updating score for user ID: {user_id} in quiz ID: {quiz_id}")
        try:
            result = await self.db.execute(
                select(Participant).filter_by(quiz_id=quiz_id, user_id=user_id)
            )
            participant = result.scalars().first()
            if participant:
                participant.score += increment
                await self.db.commit()
                self.logger.info(
                    f"Score updated to {participant.score} for user ID: {user_id} in quiz ID: {quiz_id}"
                )
                return participant.score
            self.logger.warning(
                f"Participant not found for user ID: {user_id} in quiz ID: {quiz_id}"
            )
            return 0
        except Exception as e:
            self.logger.error(
                f"Error updating score for user ID {user_id} in quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def get_leaderboard(self, quiz_id: str) -> List[dict]:
        self.logger.info(f"Fetching leaderboard for quiz ID: {quiz_id}")
        try:
            result = await self.db.execute(
                select(Participant)
                .filter_by(quiz_id=quiz_id)
                .order_by(Participant.score.desc())
            )
            participants = result.scalars().all()
            self.logger.info(f"Leaderboard retrieved for quiz ID: {quiz_id}")
            return [
                {"username": p.user.username, "score": p.score} for p in participants
            ]
        except Exception as e:
            self.logger.error(
                f"Error fetching leaderboard for quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def add_question(self, quiz_id: str, question_in: QuestionCreate) -> Question:
        self.logger.info(f"Adding question to quiz ID: {quiz_id}")
        try:
            question = Question(
                quiz_id=quiz_id,
                text=question_in.text,
                options=question_in.options,
                correct_option=question_in.correct_option,
            )
            self.db.add(question)
            await self.db.commit()
            await self.db.refresh(question)
            self.logger.info(
                f"Question added successfully to quiz ID: {quiz_id}, Question ID: {question.id}"
            )
            return question
        except Exception as e:
            self.logger.error(f"Error adding question to quiz ID {quiz_id}: {str(e)}")
            raise e

    async def get_questions(self, quiz_id: str) -> List[Question]:
        self.logger.info(f"Fetching questions for quiz ID: {quiz_id}")
        try:
            result = await self.db.execute(select(Question).filter_by(quiz_id=quiz_id))
            questions = result.scalars().all()
            self.logger.info(f"Questions retrieved successfully for quiz ID: {quiz_id}")
            return questions
        except Exception as e:
            self.logger.error(
                f"Error fetching questions for quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def get_quiz_by_id(self, quiz_id: str) -> QuizSession:
        self.logger.info(f"Fetching quiz by ID: {quiz_id}")
        try:
            result = await self.db.execute(
                select(QuizSession).filter_by(quiz_id=quiz_id)
            )
            quiz = result.scalars().first()
            if quiz:
                self.logger.info(f"Quiz retrieved successfully with ID: {quiz_id}")
            else:
                self.logger.warning(f"Quiz not found with ID: {quiz_id}")
            return quiz
        except Exception as e:
            self.logger.error(f"Error fetching quiz by ID {quiz_id}: {str(e)}")
            raise e

    async def get_participants(self, quiz_id: str) -> List[Participant]:
        self.logger.info(f"Fetching participants for quiz ID: {quiz_id}")
        try:
            result = await self.db.execute(
                select(Participant).filter_by(quiz_id=quiz_id)
            )
            participants = result.scalars().all()
            self.logger.info(
                f"Participants retrieved successfully for quiz ID: {quiz_id}"
            )
            return participants
        except Exception as e:
            self.logger.error(
                f"Error fetching participants for quiz ID {quiz_id}: {str(e)}"
            )
            raise e
