import pytest


@pytest.mark.asyncio
async def test_get_meetings(test_client):
    response = await test_client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
