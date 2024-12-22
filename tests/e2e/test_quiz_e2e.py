import os
import random
import sys

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from websockets import connect

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
# put import here to update the project folder for importing
from src.main import app
from tests.utils.string import generate_random_string

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
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    random_username = generate_random_string()
    random_password = generate_random_string()

    # Send the request with random username and password
    res = await test_app.post(
        "register",
        params={"username": random_username, "password": random_password},
        headers=headers,
    )

    print(33, res)
    assert res.status_code == 200

    # Login user

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
    user_id = res.json()["data"]["creator_user_id"]
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
    uri = f"ws://localhost:8000/ws/{quiz_id}?token={token}"
    async with connect(uri) as websocket:
        await websocket.send('{"action": "join"}')
        msg = await websocket.recv()
        assert f"User {user_id} joined quiz" in msg
