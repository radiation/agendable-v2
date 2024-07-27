import pytest
from app.crud.meeting_attendee_crud import (
    create_meeting_attendee,
    delete_meeting_attendee,
    get_meeting_attendee,
    update_meeting_attendee,
)
from app.models import MeetingAttendee
from app.schemas import meeting_attendee_schemas


async def create_test_meeting_attendee(db_session):
    meeting_attendee = MeetingAttendee(meeting_id=1, user_id=1)
    db_session.add(meeting_attendee)
    await db_session.commit()
    return meeting_attendee


@pytest.mark.asyncio
async def test_create_meeting_attendee(test_client):
    client, db_session = test_client

    new_meeting_attendee = meeting_attendee_schemas.MeetingAttendeeCreate(
        meeting_id=1, user_id=1
    )
    meeting_attendee = await create_meeting_attendee(db_session, new_meeting_attendee)
    assert meeting_attendee.meeting_id == 1

    # Refresh to get updated data
    await db_session.refresh(meeting_attendee)
    assert meeting_attendee.user_id == 1


@pytest.mark.asyncio
async def test_update_meeting_attendee(test_client):
    client, db_session = test_client

    new_meeting_attendee = MeetingAttendee(meeting_id=1, user_id=1)
    db_session.add(new_meeting_attendee)
    await db_session.commit()

    # Data to update
    update_data = meeting_attendee_schemas.MeetingAttendeeUpdate(
        meeting_id=2, user_id=1
    )
    updated_meeting_attendee = await update_meeting_attendee(
        db_session, new_meeting_attendee.id, update_data
    )
    assert updated_meeting_attendee.meeting_id == 2

    # Refresh to get updated data
    await db_session.refresh(updated_meeting_attendee)
    assert updated_meeting_attendee.meeting_id == 2


@pytest.mark.asyncio
async def test_delete_meeting_attendee(test_client):
    client, db_session = test_client

    meeting_attendee = await create_test_meeting_attendee(db_session)

    # Check that the meeting_attendee exists
    assert await get_meeting_attendee(db_session, meeting_attendee.id) is not None

    # Delete the meeting_attendee
    await delete_meeting_attendee(db_session, meeting_attendee.id)

    # Check that the meeting_attendee no longer exists
    assert await get_meeting_attendee(db_session, meeting_attendee.id) is None
