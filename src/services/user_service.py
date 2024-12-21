from werkzeug.security import check_password_hash, generate_password_hash

from src.repositories.user_repository import UserRepository
from src.utils.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, username: str, password: str):
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExistsException(
                detail=f"User '{username}' already exists."
            )

        # Create the new user
        hashed_password = generate_password_hash(password)
        new_user = await self.user_repository.create_user(username, hashed_password)
        return new_user

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException(detail=f"User '{username}' not found.")

        # Check password
        if not check_password_hash(user.password_hash, password):
            raise InvalidCredentialsException(detail="Invalid username or password.")

        return user

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(detail=f"User with ID '{user_id}' not found.")
        return user
