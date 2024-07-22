import pytest
from app.main import app
from httpx import AsyncClient

client = AsyncClient(app=app)


@pytest.mark.asyncio
async def test_create_meeting(test_client):
    response = await test_client.post(
        "/meetings/",
        json={
            "title": "Team Meeting",
            "start_date": "2024-01-01T09:00:00Z",
            "end_date": "2024-01-01T10:00:00Z",
            "duration": 60,
            "location": "Conference Room 1",
            "notes": "Monthly review meeting",
            "num_reschedules": 0,
            "reminder_sent": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Team Meeting"


@pytest.mark.asyncio
async def test_get_meetings(test_client):
    response = await test_client.get("/meetings/")
    assert response.status_code == 200
    meetings = response.json()
    assert isinstance(meetings, list)


@pytest.mark.asyncio
async def test_get_meeting(test_client):
    # Assuming there is a meeting with ID 1
    response = await test_client.get("/meetings/1")
    assert response.status_code == 200
    meeting = response.json()
    assert meeting["id"] == 1
    assert meeting["title"] == "Team Meeting"


@pytest.mark.asyncio
async def test_update_meeting(test_client):
    response = await test_client.put(
        "/meetings/1",
        json={
            "title": "Updated Team Meeting",
            "start_date": "2024-01-01T09:00:00Z",
            "end_date": "2024-01-01T10:00:00Z",
            "duration": 60,
            "location": "New Location",
            "notes": "Updated notes",
            "num_reschedules": 1,
            "reminder_sent": True,
        },
    )
    assert response.status_code == 200
    updated_meeting = response.json()
    assert updated_meeting["title"] == "Updated Team Meeting"
    assert updated_meeting["location"] == "New Location"


@pytest.mark.asyncio
async def test_delete_meeting(test_client):
    response = await test_client.delete("/meetings/1")
    assert response.status_code == 204
