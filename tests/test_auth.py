import pytest


@pytest.mark.anyio
async def test_register_success(async_client):
    url = "auth/register"
    data = {"username": "testuser1", "password": "asdfasdf", "password_repeat": "asdfasdf"}
    async with async_client as ac:
        response = await ac.post(url, json=data)
    assert response.status_code == 200, response.json()
