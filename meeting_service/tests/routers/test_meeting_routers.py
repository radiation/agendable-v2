import pytest

meeting_data = {
    "title": "Team Meeting",
    "start_date": "2024-01-01T09:00:00Z",
    "end_date": "2024-01-01T10:00:00Z",
    "duration": 60,
    "location": "Conference Room 1",
    "notes": "Monthly review meeting",
    "num_reschedules": 0,
    "reminder_sent": False,
}


@pytest.mark.asyncio
async def test_meeting_router_lifecycle(test_client):

    # Create a meeting
    response = await test_client.post(
        "/meetings/",
        json=meeting_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Team Meeting"
    meeting_id = data["id"]

    # List all meetings
    response = await test_client.get("/meetings/")
    assert response.status_code == 200
    meetings = response.json()
    assert isinstance(meetings, list)

    # Get the meeting we created
    response = await test_client.get(f"/meetings/{meeting_id}")
    assert response.status_code == 200
    meeting = response.json()
    assert meeting["id"] == 1
    assert meeting["title"] == "Team Meeting"

    # Update the meeting we created
    response = await test_client.post(
        "/meetings/",
        json=meeting_data,
    )
    meeting_id = response.json()["id"]
    response = await test_client.put(
        f"/meetings/{meeting_id}",
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

    # Delete the meeting we created
    response = await test_client.delete("/meetings/1")
    assert response.status_code == 204
