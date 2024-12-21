# src/main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.database import async_engine
from src.models.base import Base
from src.routers import auth, quiz, websocket
from src.utils.exceptions import (
    InvalidAnswerException,
    InvalidCredentialsException,
    ParticipantNotFoundException,
    QuizNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
    invalid_answer_handler,
    invalid_credentials_handler,
    participant_not_found_handler,
    quiz_not_found_handler,
    user_already_exists_handler,
    user_not_found_handler,
)
from src.utils.logger import LoggerSingleton

# Initialize Logger Singleton
logger_instance = LoggerSingleton().logger

# Create FastAPI app instance
app = FastAPI(
    title="Real-Time Quiz API",
    description="A FastAPI application for managing real-time quizzes.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize Prometheus Instrumentator **before** including routers
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Include routers
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(websocket.router)

# Register custom exception handlers
app.add_exception_handler(UserAlreadyExistsException, user_already_exists_handler)
app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(QuizNotFoundException, quiz_not_found_handler)
app.add_exception_handler(ParticipantNotFoundException, participant_not_found_handler)
app.add_exception_handler(InvalidAnswerException, invalid_answer_handler)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Real-Time Quiz API"}


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    try:
        # Uncomment if you need to create tables on startup
        # await create_tables()
        logger_instance.info("Initialize application")
        # Any additional startup tasks can be added here
    except Exception as e:
        logger_instance.error(f"Error during startup: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await async_engine.dispose()
        logger_instance.info("Database engine disposed.")
    except Exception as e:
        logger_instance.error(f"Error during shutdown: {e}")


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
