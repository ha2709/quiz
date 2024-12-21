from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    async def execute(self):
        pass
