from fastapi import APIRouter, Depends

from src.schemas.question import QuestionCreate
from src.schemas.quiz import QuizCreate
from src.services.quiz_service import QuizService
from src.utils.auth import get_current_user
from src.utils.dependencies import get_quiz_service
from src.utils.logger import LoggerSingleton
from src.utils.response import format_response

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)
logger = LoggerSingleton().logger


@router.get("/{quiz_id}/leaderboard")
async def get_leaderboard(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(f"Retrieving leaderboard for quiz ID: {quiz_id}")
        leaderboard_entries = await quiz_service.get_leaderboard(quiz_id=quiz_id)
        logger.info(f"Leaderboard retrieved successfully for quiz ID: {quiz_id}")
        return format_response(
            "success",
            "Leaderboard retrieved successfully.",
            {
                "quiz_id": quiz_id,
                "leaderboard_entries": leaderboard_entries,
            },
        )
    except Exception as e:
        logger.error(f"Error retrieving leaderboard for quiz ID {quiz_id}: {str(e)}")
        return format_response("error", str(e))


@router.post("/")
async def create_quiz(
    quiz: QuizCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(
            f"Creating quiz with ID: {quiz.quiz_id} by user ID: {current_user.id}"
        )
        new_quiz = await quiz_service.create_quiz(
            creator_id=current_user.id, quiz_id=quiz.quiz_id
        )
        logger.info(f"Quiz created successfully with ID: {new_quiz.quiz_id}")
        return format_response(
            "success",
            "Quiz created successfully.",
            {
                "quiz_id": new_quiz.quiz_id,
                "creator_user_id": new_quiz.creator_user_id,
                "status": new_quiz.status,
                "created_at": new_quiz.created_at,
            },
        )
    except Exception as e:
        logger.error(f"Error creating quiz with ID {quiz.quiz_id}: {str(e)}")
        return format_response("error", str(e))


@router.post("/{quiz_id}/questions")
async def add_question(
    quiz_id: str,
    question: QuestionCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(f"Adding question to quiz ID: {quiz_id}")
        new_question = await quiz_service.add_question_to_quiz(
            quiz_id=quiz_id,
            text=question.text,
            options=question.options,
            correct_option=question.correct_option,
        )
        logger.info(
            f"Question added successfully to quiz ID: {quiz_id}, Question ID: {new_question.id}"
        )
        return format_response(
            "success",
            "Question added successfully.",
            {
                "quiz_id": quiz_id,
                "question_id": new_question.id,
                "text": new_question.text,
                "options": new_question.options,
                "correct_option": new_question.correct_option,
            },
        )
    except Exception as e:
        logger.error(f"Error adding question to quiz ID {quiz_id}: {str(e)}")
        return format_response("error", str(e))


@router.post("/{quiz_id}/participants")
async def add_participant(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(
            f"Adding participant to quiz ID: {quiz_id} by user ID: {current_user.id}"
        )
        new_participant = await quiz_service.add_participant(
            quiz_id=quiz_id, user_id=current_user.id
        )
        logger.info(
            f"Participant added successfully to quiz ID: {quiz_id}, Participant ID: {new_participant.id}"
        )
        return format_response(
            "success",
            "Participant added successfully.",
            {
                "id": new_participant.id,
                "quiz_id": new_participant.quiz_id,
                "user_id": new_participant.user_id,
                "score": new_participant.score,
            },
        )
    except Exception as e:
        logger.error(f"Error adding participant to quiz ID {quiz_id}: {str(e)}")
        return format_response("error", str(e))


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(f"Retrieving quiz details for quiz ID: {quiz_id}")
        quiz = await quiz_service.get_quiz(quiz_id)
        logger.info(f"Quiz details retrieved successfully for quiz ID: {quiz_id}")
        return format_response(
            "success",
            "Quiz retrieved successfully.",
            {
                "quiz_id": quiz.quiz_id,
                "creator_user_id": quiz.creator_user_id,
                "status": quiz.status,
                "created_at": quiz.created_at,
            },
        )
    except Exception as e:
        logger.error(f"Error retrieving quiz details for quiz ID {quiz_id}: {str(e)}")
        return format_response("error", str(e))


@router.get("/{quiz_id}/participants")
async def get_quiz_participants(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(f"Retrieving participants for quiz ID: {quiz_id}")
        participants = await quiz_service.get_participants(quiz_id)
        logger.info(f"Participants retrieved successfully for quiz ID: {quiz_id}")
        return format_response(
            "success", "Participants retrieved successfully.", participants
        )
    except Exception as e:
        logger.error(f"Error retrieving participants for quiz ID {quiz_id}: {str(e)}")
        return format_response("error", str(e))
