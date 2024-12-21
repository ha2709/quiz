import asyncio

import pytest
from httpx import AsyncClient
from websockets import connect


@pytest.mark.asyncio
async def test_full_quiz_flow(test_app):
    # test_app is a fixture that runs FastAPI app in a test server
    async with AsyncClient(app=test_app, base_url="http://testserver") as client:
        # Register user
        res = await client.post(
            "/auth/register", json={"username": "john", "password": "secret"}
        )
        assert res.status_code == 200

        # Login user
        res = await client.post(
            "/auth/login", json={"username": "john", "password": "secret"}
        )
        assert res.status_code == 200
        token = res.json().get("token")

        # Create quiz
        headers = {"Authorization": f"Bearer {token}"}
        res = await client.post("/quiz/", headers=headers, json={"quiz_id": None})
        assert res.status_code == 200
        quiz_id = res.json()["quiz_id"]

        # Add question
        question_payload = {
            "text": "Capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "correct_option": 2,
        }
        res = await client.post(
            f"/quiz/{quiz_id}/questions", headers=headers, json=question_payload
        )
        assert res.status_code == 200

        # Test WebSocket join
        uri = f"ws://testserver/ws/{quiz_id}"
        async with connect(uri) as websocket:
            await websocket.send('{"action": "join", "user_id": 1}')
            msg = await websocket.recv()
            assert "User 1 joined quiz" in msg
