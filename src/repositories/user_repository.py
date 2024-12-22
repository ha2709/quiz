from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from werkzeug.security import check_password_hash

from src.models.user import User
from src.repositories.base_repository import BaseRepository
from src.schemas.user import UserCreate, UserUpdate
from src.utils.logger import LoggerSingleton


class UserRepository(BaseRepository[User, UserCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
        self.logger = LoggerSingleton().logger

    async def get_user_by_username(self, username: str) -> Optional[User]:
        self.logger.debug(f"Querying user by username: {username}")
        result = await self.db.execute(select(User).filter_by(username=username))
        user = result.scalars().first()
        if user:
            self.logger.debug(f"User found: {user.username}")
        else:
            self.logger.warning(f"User not found: {username}")
        return user

    async def create_user(self, username: str, password_hash: str) -> User:
        self.logger.debug(f"Creating user: {username} - {password_hash}")
        user_data = UserCreate(username=username, password_hash=password_hash)
        user = await self.create(user_data)  # Use BaseRepository's create method
        self.logger.info(f"User created with ID: {user.id}")
        return user

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        self.logger.info(f"Authenticating user: {username}")
        user = await self.get_user_by_username(username)
        if user:
            if check_password_hash(user.password_hash, password):
                self.logger.info(f"Authentication successful for user: {username}")
                return user
            else:
                self.logger.warning(
                    f"Authentication failed - invalid password for user: {username}"
                )
        else:
            self.logger.warning(f"Authentication failed - user not found: {username}")
        return None

    async def get_user_by_id(self, user_id: int) -> User:
        self.logger.info(f"Fetching user by ID: {user_id}")
        user = await self.get(user_id)  # Use BaseRepository's get method
        if user:
            self.logger.info(f"User fetched successfully with ID: {user_id}")
        else:
            self.logger.warning(
                f"User fetch failed - user with ID {user_id} not found."
            )
        return user
