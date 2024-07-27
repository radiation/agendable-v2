import pytest


@pytest.mark.asyncio
async def test_get_meeting_recurrences(test_client):
    client, db_session = test_client

    response = await client.get("/meeting_recurrences/")
    assert response.status_code == 200
    meeting_recurrences = response.json()
    assert isinstance(meeting_recurrences, list)
