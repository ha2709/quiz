import os
import random
import sys

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from websockets import connect

from src.main import app

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)


load_dotenv()
BASE_URL = os.getenv("BASE_URL")
print(14, BASE_URL)


@pytest.fixture
async def test_app():

    # Use ASGITransport to connect the AsyncClient to the FastAPI app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        yield client


@pytest.mark.asyncio
async def test_full_quiz_flow(test_app):
    # Register user
    # res = await test_app.post(
    #     "register",
    #     params={"username": "john1", "password": "secret1"},
    #     headers=HEADERS,
    # )
    # print(33, res)
    # assert res.status_code == 200

    # Login user
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = await test_app.post(
        "auth/token",
        data={"username": "john1", "password": "secret1"},
        headers=headers,
    )
    print(48, res.json())
    assert res.status_code == 200
    token = res.json().get("data").get("access_token")
    print(55, token)
    # Create quiz
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

    # Generate a random quiz ID
    random_quiz_id = str(random.randint(10000, 99999))
    res = await test_app.post(
        "quiz/", headers=headers, json={"quiz_id": str(random_quiz_id)}
    )
    print(60, res.json())
    assert res.status_code == 200

    quiz_id = res.json()["data"]["quiz_id"]
    print(63, quiz_id)
    # Add question
    question_payload = {
        "text": "Capital of France?",
        "options": "Berlin, Madrid, Paris, Rome",
        "correct_option": 2,
    }
    res = await test_app.post(
        f"/quiz/{quiz_id}/questions", headers=headers, json=question_payload
    )
    assert res.status_code == 200

    # # Test WebSocket join
    uri = f"ws://localhost:8000/ws/{quiz_id}"
    async with connect(uri) as websocket:
        await websocket.send('{"action": "join", "user_id": 1}')
        msg = await websocket.recv()
        assert "User 1 joined quiz" in msg
