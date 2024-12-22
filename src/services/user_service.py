from werkzeug.security import check_password_hash, generate_password_hash

from src.repositories.user_repository import UserRepository
from src.utils.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.utils.logger import LoggerSingleton


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.logger = LoggerSingleton().logger

    async def create_user(self, username: str, password: str):
        self.logger.info(f"Creating user: {username}")
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_username(username)
        if existing_user:
            self.logger.warning(
                f"User creation failed. User '{username}' already exists."
            )
            raise UserAlreadyExistsException(
                detail=f"User '{username}' already exists."
            )

        # Create the new user
        hashed_password = generate_password_hash(password)
        print(31, hashed_password)
        if not hashed_password:
            self.logger.error(f"Password hashing failed for user: {username}")
            raise Exception("Password hashing returned null or empty string")

        self.logger.debug(f"Hashed password for user {username}: {hashed_password}")

        new_user = await self.user_repository.create_user(username, hashed_password)
        self.logger.info(f"User created with ID: {new_user.id}")
        return new_user

    async def authenticate_user(self, username: str, password: str):
        self.logger.info(f"Authenticating user: {username}")
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            self.logger.warning(f"Authentication failed for user: {username}")
            raise UserNotFoundException(detail=f"User '{username}' not found.")

        # Check password
        if not check_password_hash(user.password_hash, password):
            self.logger.warning(
                f"Authentication failed. Invalid password for user: {username}"
            )
            raise InvalidCredentialsException(detail="Invalid username or password.")

        self.logger.info(f"Authentication successful for user: {username}")
        return user

    async def get_user_by_id(self, user_id: int):
        self.logger.info(f"Fetching user with ID: {user_id}")
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            self.logger.warning(
                f"User fetch failed. User with ID '{user_id}' not found."
            )
            raise UserNotFoundException(detail=f"User with ID '{user_id}' not found.")

        self.logger.info(f"User fetched successfully with ID: {user_id}")
        return user
