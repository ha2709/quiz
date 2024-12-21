from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from werkzeug.security import check_password_hash

from src.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str) -> Optional[User]:
        # Use `select` for async queries
        result = await self.db.execute(select(User).filter_by(username=username))
        return result.scalars().first()

    async def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.db.execute(select(User).filter_by(id=user_id))
        return result.scalars().first()
