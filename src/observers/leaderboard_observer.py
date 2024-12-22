from typing import List

from fastapi import WebSocket

from src.observers.base_observer import BaseObserver
from src.utils.logger import LoggerSingleton


class LeaderboardObserver(BaseObserver):
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.logger = LoggerSingleton().logger

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(
            f"New WebSocket connection added. Total connections: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.logger.info(
                f"WebSocket connection removed. Total connections: {len(self.active_connections)}"
            )
        else:
            self.logger.warning(
                "Attempted to remove a non-existent WebSocket connection."
            )

    async def notify(self, data: dict):
        self.logger.info(
            f"Broadcasting data to {len(self.active_connections)} active connections."
        )
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
                self.logger.debug(f"Data sent to connection: {connection.client}")
            except Exception as e:
                self.logger.error(
                    f"Error sending data to connection {connection.client}: {str(e)}"
                )
                disconnected_clients.append(connection)

        # Remove disconnected clients
        for connection in disconnected_clients:
            self.disconnect(connection)

    # def update(self, data: dict):
    #     pass
