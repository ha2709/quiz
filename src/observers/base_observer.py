from abc import ABC, abstractmethod


class BaseObserver(ABC):
    @abstractmethod
    async def update(self, data: dict):
        pass
