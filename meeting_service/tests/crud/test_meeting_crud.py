from datetime import datetime, timedelta

import pytest
from app.crud.meeting_crud import (
    create_meeting,
    delete_meeting,
    get_meeting,
    update_meeting,
)
from app.models import Meeting
from app.schemas import meeting_schemas


async def create_test_meeting(db_session, title="Test Meeting"):
    meeting = Meeting(title=title)
    db_session.add(meeting)
    await db_session.commit()
    return meeting


@pytest.mark.asyncio
async def test_create_meeting(test_client):
    client, db_session = test_client

    new_meeting = meeting_schemas.MeetingCreate(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    meeting = await create_meeting(db_session, new_meeting)
    assert meeting.title == "Test Meeting"

    # Refresh to get updated data
    await db_session.refresh(meeting)
    assert meeting.title == "Test Meeting"


@pytest.mark.asyncio
async def test_update_meeting(test_client):
    client, db_session = test_client

    new_meeting = Meeting(
        title="Initial Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
    )
    db_session.add(new_meeting)
    await db_session.commit()

    # Data to update
    update_data = meeting_schemas.MeetingUpdate(title="Updated Meeting")
    updated_meeting = await update_meeting(db_session, new_meeting.id, update_data)
    assert updated_meeting.title == "Updated Meeting"

    # Refresh to get updated data
    await db_session.refresh(updated_meeting)
    assert updated_meeting.title == "Updated Meeting"


@pytest.mark.asyncio
async def test_delete_meeting(test_client):
    client, db_session = test_client

    meeting = await create_test_meeting(db_session)

    # Check that the meeting exists
    assert await get_meeting(db_session, meeting.id) is not None

    # Delete the meeting
    await delete_meeting(db_session, meeting.id)

    # Check that the meeting no longer exists
    assert await get_meeting(db_session, meeting.id) is None
