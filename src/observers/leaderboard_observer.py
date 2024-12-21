from typing import List

from fastapi import WebSocket

from src.observers.base_observer import BaseObserver
from src.services.quiz_service import QuizService


class LeaderboardObserver(BaseObserver):
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def notify(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    def update(self, data: dict):
        # This method can be expanded if needed
        pass
