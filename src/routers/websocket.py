import json
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from src.schemas.leaderboard import Leaderboard
from src.services.quiz_service import QuizService
from src.services.user_service import UserService
from src.utils.auth import get_current_user_for_ws
from src.utils.dependencies import get_quiz_service, get_user_service
from src.utils.exceptions import QuizNotFoundException
from src.utils.logger import LoggerSingleton

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)
logger = LoggerSingleton().logger


# In-memory storage of active connections per quiz
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, quiz_id: str, websocket: WebSocket):
        await websocket.accept()
        if quiz_id not in self.active_connections:
            self.active_connections[quiz_id] = []
        self.active_connections[quiz_id].append(websocket)
        logger.info(f"WebSocket connection established for quiz ID: {quiz_id}")

    def disconnect(self, quiz_id: str, websocket: WebSocket):
        self.active_connections[quiz_id].remove(websocket)
        if not self.active_connections[quiz_id]:
            del self.active_connections[quiz_id]
        logger.info(f"WebSocket connection closed for quiz ID: {quiz_id}")

    async def broadcast_leaderboard(self, quiz_id: str, leaderboard: Leaderboard):
        if quiz_id in self.active_connections:
            message = json.dumps(
                {"type": "leaderboard_update", "data": leaderboard.dict()}
            )
            for connection in self.active_connections[quiz_id]:
                await connection.send_text(message)
            logger.info(f"Broadcasted leaderboard update for quiz ID: {quiz_id}")


manager = ConnectionManager()


@router.websocket("/{quiz_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    quiz_id: str,
    quiz_service: QuizService = Depends(get_quiz_service),
    user_service: UserService = Depends(get_user_service),
):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Missing token")
        logger.warning("WebSocket connection rejected due to missing token.")
        return

    try:
        current_user = await get_current_user_for_ws(
            token=token, user_service=user_service
        )
    except HTTPException as e:
        await websocket.close(code=1008, reason=str(e.detail))
        logger.warning(f"WebSocket connection rejected: {e.detail}")
        return
    await manager.connect(quiz_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(f"Received WebSocket message for quiz ID {quiz_id}: {message}")
            action = message.get("action")
            if action == "submit_answer":
                user_id = message.get("user_id")
                question_id = message.get("question_id")
                selected_option = message.get("selected_option")

                # Process the answer, fetch the question and verify the answer

                # Update participant's score if the answer is correct
                try:
                    participant = await quiz_service.update_score(
                        quiz_id=quiz_id, user_id=user_id, increment=1
                    )
                    logger.info(f"Score updated for user {user_id} in quiz {quiz_id}")
                except ValueError as e:
                    error_message = str(e)
                    logger.error(f"Error updating score: {error_message}")
                    await websocket.send_text(
                        json.dumps({"type": "error", "message": error_message})
                    )
                    continue

                # Fetch the updated leaderboard
                leaderboard_entries = await quiz_service.get_leaderboard(
                    quiz_id=quiz_id
                )
                leaderboard = Leaderboard(quiz_id=quiz_id, entries=leaderboard_entries)

                # Broadcast the updated leaderboard to all connected clients
                await manager.broadcast_leaderboard(quiz_id, leaderboard)

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

                user_id = current_user.id
                logger.info(f"User {user_id} joined quiz {quiz_id}")
                # Validate the quiz exists
                try:
                    await quiz_service.get_quiz(quiz_id)
                except QuizNotFoundException:
                    error_message = f"Quiz {quiz_id} does not exist."
                    logger.warning(error_message)
                    await websocket.send_text(
                        json.dumps({"type": "error", "message": error_message})
                    )
                    return

                # Optionally, validate the user exists

                if not await user_service.get_user_by_id(user_id):
                    error_message = f"User {user_id} does not exist."
                    logger.warning(error_message)
                    await websocket.send_text(
                        json.dumps({"type": "error", "message": error_message})
                    )
                    return

                logger.info(f"User {user_id} successfully joined quiz {quiz_id}")
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
                logger.info(f"Quiz {quiz_id} started and leaderboard broadcasted")

            else:
                logger.warning(
                    f"Invalid action received for quiz ID {quiz_id}: {action}"
                )
                await websocket.send_text(
                    json.dumps({"type": "error", "message": "Invalid action."})
                )
    except WebSocketDisconnect:
        manager.disconnect(quiz_id, websocket)
        logger.info(f"WebSocket disconnected for quiz ID {quiz_id}")

        leaderboard_entries = await quiz_service.get_leaderboard(quiz_id=quiz_id)
        await manager.broadcast_leaderboard(quiz_id, leaderboard_entries)
