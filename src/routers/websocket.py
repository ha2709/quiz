import json
from typing import Dict, List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)

from src.schemas.leaderboard import Leaderboard
from src.services.quiz_service import QuizService
from src.utils.dependencies import get_quiz_service

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)


# In-memory storage of active connections per quiz
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, quiz_id: str, websocket: WebSocket):
        await websocket.accept()
        if quiz_id not in self.active_connections:
            self.active_connections[quiz_id] = []
        self.active_connections[quiz_id].append(websocket)

    def disconnect(self, quiz_id: str, websocket: WebSocket):
        self.active_connections[quiz_id].remove(websocket)
        if not self.active_connections[quiz_id]:
            del self.active_connections[quiz_id]

    async def broadcast_leaderboard(self, quiz_id: str, leaderboard: Leaderboard):
        if quiz_id in self.active_connections:
            message = json.dumps(
                {"type": "leaderboard_update", "data": leaderboard.dict()}
            )
            for connection in self.active_connections[quiz_id]:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/{quiz_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
):
    await manager.connect(quiz_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            action = message.get("action")
            if action == "submit_answer":
                user_id = message.get("user_id")
                question_id = message.get("question_id")
                selected_option = message.get("selected_option")

                # Process the answer

                # For demonstration, let's assume any selected_option is correct
                # In practice, fetch the question and verify the answer

                # Update participant's score if the answer is correct
                try:
                    participant = await quiz_service.update_score(
                        quiz_id=quiz_id, user_id=user_id, score_increment=1
                    )
                except ValueError as e:
                    await websocket.send_text(
                        json.dumps({"type": "error", "message": str(e)})
                    )
                    continue

                # Fetch the updated leaderboard
                leaderboard_entries = await quiz_service.get_leaderboard(
                    quiz_id=quiz_id
                )
                leaderboard = Leaderboard(quiz_id=quiz_id, entries=leaderboard_entries)

                # Broadcast the updated leaderboard to all connected clients
                await manager.broadcast_leaderboard(quiz_id, leaderboard)

                # Optionally, send acknowledgment to the sender
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "answer_result",
                            "data": {
                                "question_id": question_id,
                                "result": "correct",  # or "incorrect" based on actual answer
                            },
                        }
                    )
                )

            elif action == "join":
                # Handle participant joining the quiz
                user_id = message.get("user_id")
                # Optionally, verify if the user is part of the quiz
                # For now, simply acknowledge the join
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "status",
                            "message": f"User {user_id} joined quiz {quiz_id}.",
                        }
                    )
                )

            elif action == "start_quiz":
                # Handle starting the quiz
                # For demonstration, we'll just broadcast the current leaderboard
                leaderboard_entries = await quiz_service.get_leaderboard(
                    quiz_id=quiz_id
                )
                leaderboard = Leaderboard(quiz_id=quiz_id, entries=leaderboard_entries)
                await manager.broadcast_leaderboard(quiz_id, leaderboard)

            else:
                await websocket.send_text(
                    json.dumps({"type": "error", "message": "Invalid action."})
                )
    except WebSocketDisconnect:
        manager.disconnect(quiz_id, websocket)
        # Optionally, broadcast that a user has disconnected
        await manager.broadcast_leaderboard(
            quiz_id, await quiz_service.get_leaderboard(quiz_id)
        )
