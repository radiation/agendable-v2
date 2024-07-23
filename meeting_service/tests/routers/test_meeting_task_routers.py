import pytest


@pytest.mark.asyncio
async def test_get_meeting_tasks(test_client):
    response = await test_client.get("/tasks/")
    assert response.status_code == 200
    meeting_tasks = response.json()
    assert isinstance(meeting_tasks, list)
