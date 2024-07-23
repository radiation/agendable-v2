import pytest


@pytest.mark.asyncio
async def test_get_meeting_attendees(test_client):
    response = await test_client.get("/tasks/")
    assert response.status_code == 200
    meeting_attendees = response.json()
    assert isinstance(meeting_attendees, list)
