from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")  # SQLAlchemy model
P = TypeVar("P")  # Pydantic schema


class BaseRepository(Generic[T, P]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: int) -> Optional[T]:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: P) -> T:
        obj = self.model(**obj_in.dict())
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, db_obj: T, obj_in: P) -> T:
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return True
        return False
