from httpx import ASGITransport, AsyncClient
import pytest

from src.main import app


@pytest.fixture
async def async_client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture
def anyio_backend():
    return "asyncio"
