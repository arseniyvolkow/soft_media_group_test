import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from dependencies import get_link_service
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_link_service():
    service = AsyncMock()
    return service


@pytest.mark.asyncio
async def test_shorten_url_api(mock_link_service):
    # Подменяем зависимость
    mock_link_service.create_short_link.return_value = "abc"
    app.dependency_overrides[get_link_service] = lambda: mock_link_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/shorten", json={"original_url": "http://google.com"})

    assert response.status_code == 200
    assert response.json()["short_id"] == "abc"
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_redirect_api(mock_link_service):
    mock_link_service.get_original_url_and_increment.return_value = "http://google.com"
    app.dependency_overrides[get_link_service] = lambda: mock_link_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/abc", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://google.com"
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_stats_api_not_found(mock_link_service):
    mock_link_service.get_stats.return_value = None
    app.dependency_overrides[get_link_service] = lambda: mock_link_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/stats/notfound")

    assert response.status_code == 404
    app.dependency_overrides.clear()
