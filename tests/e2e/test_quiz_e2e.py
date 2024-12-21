import asyncio
import os
import sys

import pytest
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from httpx import AsyncClient
from websockets import connect

# Add the path to the project's src directory to the system path
sys.path.append("/home/ha/Downloads/programs/coding-challenges-main/")
from src.main import app

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
print(14, BASE_URL)
HEADERS = {"accept": "application/json"}


@pytest.fixture
async def test_app():
    from httpx import ASGITransport

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
    HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = await test_app.post(
        "auth/token",
        data={"username": "john1", "password": "secret1"},
        headers=HEADERS,
    )
    print(48, res.json())
    assert res.status_code == 200
    token = res.json().get("access_token")
    print(55, token)
    # Create quiz
    # headers = {"Authorization": f"Bearer {token}"}
    # res = await test_app.post("quiz/", headers=headers, params={"quiz_id": "213"})
    # assert res.status_code == 200
    # quiz_id = res.json()["quiz_id"]

    # Add question
    # question_payload = {
    #     "text": "Capital of France?",
    #     "options": ["Berlin", "Madrid", "Paris", "Rome"],
    #     "correct_option": 2,
    # }
    # res = await test_app.post(
    #     f"/quiz/{quiz_id}/questions", headers=headers, json=question_payload
    # )
    # assert res.status_code == 200

    # # Test WebSocket join
    # uri = f"ws://testserver/ws/{quiz_id}"
    # async with connect(uri) as websocket:
    #     await websocket.send('{"action": "join", "user_id": 1}')
    #     msg = await websocket.recv()
    #     assert "User 1 joined quiz" in msg
