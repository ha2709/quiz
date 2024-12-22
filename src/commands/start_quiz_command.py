import asyncio

from src.commands.base_command import BaseCommand
from src.observers.leaderboard_observer import LeaderboardObserver
from src.services.quiz_service import QuizService
from src.utils.logger import LoggerSingleton


class StartQuizCommand(BaseCommand):
    def __init__(
        self, quiz_service: QuizService, quiz_id: str, observer: LeaderboardObserver
    ):
        self.quiz_service = quiz_service
        self.quiz_id = quiz_id
        self.observer = observer
        self.logger = LoggerSingleton().logger

    async def execute(self):
        self.logger.info(f"Starting quiz with ID: {self.quiz_id}")
        try:
            self.quiz_service.start_quiz(self.quiz_id)
            self.logger.info(f"Quiz {self.quiz_id} started successfully")
            # Fetch questions and emit them sequentially
            questions = self.quiz_service.quiz_repository.get_questions(self.quiz_id)
            for question in questions:
                data = {
                    "id": question.id,
                    "text": question.text,
                    "options": question.options,
                }
                self.logger.info(
                    f"Broadcasting question ID: {question.id} for quiz ID: {self.quiz_id}"
                )
                await self.observer.notify({"new_question": data})
                await asyncio.sleep(10)  # Wait for 10 seconds before next question
            self.logger.info(f"Quiz {self.quiz_id} has ended")
            await self.observer.notify({"quiz_end": "Quiz has ended!"})
        except Exception as e:
            self.logger.error(
                f"Error executing StartQuizCommand for quiz ID {self.quiz_id}: {str(e)}"
            )
            raise
