from typing import List

from fastapi import APIRouter, Depends

from src.schemas.leaderboard import Leaderboard
from src.schemas.participant import ParticipantRead
from src.schemas.question import QuestionCreate
from src.schemas.quiz import QuizCreate, QuizRead
from src.services.quiz_service import QuizService
from src.utils.auth import get_current_user
from src.utils.dependencies import get_quiz_service
from src.utils.response import format_response

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


@router.get("/{quiz_id}/leaderboard")
async def get_leaderboard(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # If the quiz doesn't exist, QuizService will raise QuizNotFoundException
    try:
        # Retrieve leaderboard entries
        leaderboard_entries = await quiz_service.get_leaderboard(quiz_id=quiz_id)
        # Format response with quiz_id and leaderboard_entries
        return format_response(
            "success",
            "Leaderboard retrieved successfully.",
            {
                "quiz_id": quiz_id,
                "leaderboard_entries": leaderboard_entries,
            },
        )
    except Exception as e:
        return format_response("error", str(e))


@router.post("/")
async def create_quiz(
    quiz: QuizCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # Use current_user.id as the creator_user_id
    new_quiz = await quiz_service.create_quiz(
        creator_id=current_user.id, quiz_id=quiz.quiz_id
    )
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


@router.post("/{quiz_id}/questions")
async def add_question(
    quiz_id: str,
    question: QuestionCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # QuizService will raise QuizNotFoundException if quiz doesn't exist
    try:
        new_question = await quiz_service.add_question_to_quiz(
            quiz_id=quiz_id,
            text=question.text,
            options=question.options,
            correct_option=question.correct_option,
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
        return format_response("error", str(e))


@router.post("/{quiz_id}/participants")
async def add_participant(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # QuizService will raise QuizNotFoundException if quiz doesn't exist
    try:
        new_participant = await quiz_service.add_participant(
            quiz_id=quiz_id, user_id=current_user.id
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
        return format_response("error", str(e))


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # QuizService will raise QuizNotFoundException if quiz doesn't exist
    try:
        quiz = await quiz_service.get_quiz(quiz_id)
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
        return format_response("error", str(e))


@router.get("/{quiz_id}/participants")
async def get_quiz_participants(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # If the quiz doesn't exist, QuizService will raise QuizNotFoundException
    try:
        participants = await quiz_service.get_participants(quiz_id)
        return format_response(
            "success", "Participants retrieved successfully.", participants
        )
    except Exception as e:
        return format_response("error", str(e))
