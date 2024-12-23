import os

import httpx
import pytest
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


@pytest.mark.asyncio
async def test_metrics_endpoint(test_app):
    async with httpx.AsyncClient(app=test_app, base_url=BASE_URL) as client:
        res = await client.get("/metrics")
        assert res.status_code == 200
        assert "http_request_duration_seconds" in res.text
