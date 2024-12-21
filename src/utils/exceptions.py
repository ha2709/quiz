from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.utils.logger import LoggerSingleton

logger_instance = LoggerSingleton().logger


class UserAlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "User already exists."):
        super().__init__(status_code=400, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(status_code=404, detail=detail)


class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials."):
        super().__init__(status_code=401, detail=detail)


class QuizNotFoundException(HTTPException):
    def __init__(self, detail: str = "Quiz not found."):
        super().__init__(status_code=404, detail=detail)


class ParticipantNotFoundException(HTTPException):
    def __init__(self, detail: str = "Participant not found."):
        super().__init__(status_code=404, detail=detail)


class InvalidAnswerException(HTTPException):
    def __init__(self, detail: str = "Invalid answer submitted."):
        super().__init__(status_code=400, detail=detail)


async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsException
):
    logger_instance.warning(f"User already exists: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    logger_instance.warning(f"User not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def quiz_not_found_handler(request: Request, exc: QuizNotFoundException):
    logger_instance.warning(f"Quiz not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def participant_not_found_handler(
    request: Request, exc: ParticipantNotFoundException
):
    logger_instance.warning(f"Participant not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def invalid_answer_handler(request: Request, exc: InvalidAnswerException):
    logger_instance.warning(f"Invalid answer: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsException
):
    logger_instance.warning(f"Invalid credentials: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(UserAlreadyExistsException, user_already_exists_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_handler)
    app.add_exception_handler(QuizNotFoundException, quiz_not_found_handler)
    app.add_exception_handler(
        ParticipantNotFoundException, participant_not_found_handler
    )
    app.add_exception_handler(InvalidAnswerException, invalid_answer_handler)
