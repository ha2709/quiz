import httpx
import pytest


@pytest.mark.asyncio
async def test_metrics_endpoint(test_app):
    async with httpx.AsyncClient(app=test_app, base_url="http://testserver") as client:
        res = await client.get("/metrics")
        assert res.status_code == 200
        assert "http_request_duration_seconds" in res.text
