from typing import List

from src.models import Participant, Question, QuizSession
from src.repositories.quiz_repository import QuizRepository
from src.schemas.question import QuestionCreate
from src.utils.exceptions import QuizNotFoundException
from src.utils.logger import LoggerSingleton


class QuizService:
    def __init__(self, quiz_repository: QuizRepository):
        self.quiz_repository = quiz_repository
        self.logger = LoggerSingleton().logger

    async def create_quiz(self, creator_id: int, quiz_id: str = None):
        self.logger.info(f"Creating quiz with ID: {quiz_id} by user ID: {creator_id}")
        try:
            quiz = await self.quiz_repository.create_quiz(
                quiz_id=quiz_id, creator_id=creator_id
            )
            self.logger.info(f"Quiz created successfully with ID: {quiz.quiz_id}")
            return quiz
        except Exception as e:
            self.logger.error(f"Error creating quiz with ID {quiz_id}: {str(e)}")
            raise e

    async def add_question_to_quiz(
        self, quiz_id: str, text: str, options: str, correct_option: int
    ):
        self.logger.info(f"Adding question to quiz ID: {quiz_id}")
        try:
            await self.get_quiz(quiz_id)  # Ensure the quiz exists
            question = await self.quiz_repository.add_question(
                quiz_id,
                QuestionCreate(
                    text=text, options=options, correct_option=correct_option
                ),
            )
            self.logger.info(
                f"Question added to quiz ID: {quiz_id}, Question ID: {question.id}"
            )
            return question
        except Exception as e:
            self.logger.error(f"Error adding question to quiz ID {quiz_id}: {str(e)}")
            raise e

    async def get_quiz(self, quiz_id: str) -> QuizSession:
        self.logger.info(f"Retrieving quiz with ID: {quiz_id}")
        try:
            quiz = await self.quiz_repository.get_quiz_by_id(quiz_id)
            if not quiz:
                self.logger.warning(f"Quiz with ID {quiz_id} not found")
                raise QuizNotFoundException(detail=f"Quiz {quiz_id} not found.")
            self.logger.info(f"Quiz retrieved successfully with ID: {quiz_id}")
            return quiz
        except Exception as e:
            self.logger.error(f"Error retrieving quiz with ID {quiz_id}: {str(e)}")
            raise e

    async def add_participant(self, quiz_id: str, user_id: int) -> Participant:
        self.logger.info(
            f"Adding participant to quiz ID: {quiz_id} by user ID: {user_id}"
        )
        try:
            await self.get_quiz(quiz_id)  # Ensure quiz exists
            participant = await self.quiz_repository.add_participant(quiz_id, user_id)
            self.logger.info(
                f"Participant added successfully: Participant ID: {participant.id}"
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
            await self.get_quiz(quiz_id)  # Ensure quiz exists
            score = await self.quiz_repository.update_score(quiz_id, user_id, increment)
            self.logger.info(
                f"Score updated for user ID: {user_id} in quiz ID: {quiz_id}. New score: {score}"
            )
            return score
        except Exception as e:
            self.logger.error(
                f"Error updating score for user ID {user_id} in quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def get_leaderboard(self, quiz_id: str) -> List[dict]:
        self.logger.info(f"Retrieving leaderboard for quiz ID: {quiz_id}")
        try:
            await self.get_quiz(quiz_id)  # Ensure quiz exists
            leaderboard = await self.quiz_repository.get_leaderboard(quiz_id)
            self.logger.info(
                f"Leaderboard retrieved successfully for quiz ID: {quiz_id}"
            )
            return leaderboard
        except Exception as e:
            self.logger.error(
                f"Error retrieving leaderboard for quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def add_question(self, quiz_id: str, question_in: QuestionCreate) -> Question:
        self.logger.info(f"Adding question to quiz ID: {quiz_id}")
        try:
            await self.get_quiz(quiz_id)  # Ensure quiz exists
            question = await self.quiz_repository.add_question(quiz_id, question_in)
            self.logger.info(
                f"Question added successfully to quiz ID: {quiz_id}, Question ID: {question.id}"
            )
            return question
        except Exception as e:
            self.logger.error(f"Error adding question to quiz ID {quiz_id}: {str(e)}")
            raise e

    async def get_questions(self, quiz_id: str) -> List[Question]:
        self.logger.info(f"Retrieving questions for quiz ID: {quiz_id}")
        try:
            await self.get_quiz(quiz_id)  # Ensure quiz exists
            questions = await self.quiz_repository.get_questions(quiz_id)
            self.logger.info(f"Questions retrieved successfully for quiz ID: {quiz_id}")
            return questions
        except Exception as e:
            self.logger.error(
                f"Error retrieving questions for quiz ID {quiz_id}: {str(e)}"
            )
            raise e

    async def get_participants(self, quiz_id: str) -> List[Participant]:
        self.logger.info(f"Retrieving participants for quiz ID: {quiz_id}")
        try:
            participants = await self.quiz_repository.get_participants(quiz_id)
            self.logger.info(
                f"Participants retrieved successfully for quiz ID: {quiz_id}"
            )
            return participants
        except Exception as e:
            self.logger.error(
                f"Error retrieving participants for quiz ID {quiz_id}: {str(e)}"
            )
            raise e
