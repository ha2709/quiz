import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# from src.models import participant, question, quiz, user
# from src.models.base imposrt Base

# Load environment variables from .env
load_dotenv()


# Asynchronous Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
)

# Synchronous Database URL for Alembic
DATABASE_URL_SYNC = os.getenv(
    "DATABASE_URL_SYNC", "postgresql+psycopg2://postgres:1234@localhost/quiz"
)
print(18, DATABASE_URL_SYNC)
# Create the asynchronous engine
async_engine = create_async_engine(
    DATABASE_URL, echo=True, future=True  # Set to False in production
)


sync_engine = create_engine(
    DATABASE_URL_SYNC, echo=True, pool_pre_ping=True  # Set to False in production
)

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Create a configured "Session" class for synchronous operations
SessionLocal = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False)
