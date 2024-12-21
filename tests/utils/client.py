import asyncio
import os

import pytest
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from httpx import AsyncClient

from src.main import app

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
print(14, BASE_URL)


@pytest.fixture
async def test_app():
    async with LifespanManager(app):  # Ensures app lifespan events are triggered
        async with AsyncClient(app=app, base_url=BASE_URL) as client:
            yield client
