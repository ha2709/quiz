from typing import List

from fastapi import APIRouter, Depends

from src.schemas.leaderboard import Leaderboard
from src.schemas.participant import ParticipantRead
from src.schemas.question import QuestionCreate
from src.schemas.quiz import QuizCreate, QuizRead
from src.services.quiz_service import QuizService
from src.utils.auth import get_current_user
from src.utils.dependencies import get_quiz_service

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


@router.get("/{quiz_id}/leaderboard", response_model=Leaderboard)
async def get_leaderboard(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    # current_user=Depends(get_current_user),
):
    # If the quiz doesn't exist, QuizService will raise QuizNotFoundException
    leaderboard_entries = await quiz_service.get_leaderboard(quiz_id=quiz_id)
    return Leaderboard(quiz_id=quiz_id, entries=leaderboard_entries)


@router.post("/", response_model=QuizRead)
async def create_quiz(
    creator_id: int,
    quiz_in: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    # current_user=Depends(get_current_user),
):
    # Use current_user.id as the creator_user_id
    new_quiz = await quiz_service.create_quiz(creator_id=creator_id, quiz_in=quiz_in)
    return new_quiz


@router.post("/{quiz_id}/questions", response_model=QuestionCreate)
async def add_question(
    quiz_id: str,
    question: QuestionCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # QuizService will raise QuizNotFoundException if quiz doesn't exist
    new_question = await quiz_service.add_question_to_quiz(
        quiz_id=quiz_id,
        text=question.text,
        options=question.options,
        correct_option=question.correct_option,
    )
    return new_question


@router.post("/{quiz_id}/participants", response_model=ParticipantRead)
async def add_participant(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # QuizService will raise QuizNotFoundException if quiz doesn't exist
    new_participant = await quiz_service.add_participant(
        quiz_id=quiz_id, user_id=current_user.id
    )
    return new_participant


@router.get("/{quiz_id}", response_model=QuizRead)
async def get_quiz(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # QuizService will raise QuizNotFoundException if quiz doesn't exist
    quiz = await quiz_service.get_quiz(quiz_id)
    return quiz


@router.get("/{quiz_id}/participants", response_model=List[ParticipantRead])
async def get_quiz_participants(
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user=Depends(get_current_user),
):
    # If the quiz doesn't exist, QuizService will raise QuizNotFoundException
    participants = await quiz_service.get_participants(quiz_id)
    return participants
