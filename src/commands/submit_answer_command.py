from src.commands.base_command import BaseCommand
from src.observers.leaderboard_observer import LeaderboardObserver
from src.services.quiz_service import QuizService
from src.utils.logger import LoggerSingleton


class SubmitAnswerCommand(BaseCommand):
    def __init__(
        self,
        quiz_service: QuizService,
        quiz_id: str,
        user_id: int,
        question_id: int,
        selected_option: int,
        observer: LeaderboardObserver,
    ):
        self.quiz_service = quiz_service
        self.quiz_id = quiz_id
        self.user_id = user_id
        self.question_id = question_id
        self.selected_option = selected_option
        self.observer = observer
        self.logger = LoggerSingleton().logger

    async def execute(self):
        self.logger.info(
            f"Executing SubmitAnswerCommand: quiz_id={self.quiz_id}, user_id={self.user_id}, question_id={self.question_id}, selected_option={self.selected_option}"
        )
        try:
            result = self.quiz_service.submit_answer(
                quiz_id=self.quiz_id,
                user_id=self.user_id,
                question_id=self.question_id,
                selected_option=self.selected_option,
            )
            self.logger.info(
                f"Answer submitted successfully for user_id={self.user_id} in quiz_id={self.quiz_id}"
            )
            await self.observer.notify({"answer_result": result})
        except Exception as e:
            self.logger.error(f"Error executing SubmitAnswerCommand: {str(e)}")
            raise
