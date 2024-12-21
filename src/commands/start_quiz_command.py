import asyncio

from src.commands.base_command import BaseCommand
from src.observers.leaderboard_observer import LeaderboardObserver
from src.services.quiz_service import QuizService


class StartQuizCommand(BaseCommand):
    def __init__(
        self, quiz_service: QuizService, quiz_id: str, observer: LeaderboardObserver
    ):
        self.quiz_service = quiz_service
        self.quiz_id = quiz_id
        self.observer = observer

    async def execute(self):
        self.quiz_service.start_quiz(self.quiz_id)
        # Fetch questions and emit them sequentially
        questions = self.quiz_service.quiz_repository.get_questions(self.quiz_id)
        for question in questions:
            data = {
                "id": question.id,
                "text": question.text,
                "options": question.options,
            }
            await self.observer.notify({"new_question": data})
            await asyncio.sleep(10)  # Wait for 10 seconds before next question
        await self.observer.notify({"quiz_end": "Quiz has ended!"})
