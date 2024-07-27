import pytest
from app.crud.meeting_recurrence_crud import (
    create_meeting_recurrence,
    delete_meeting_recurrence,
    get_meeting_recurrence,
    update_meeting_recurrence,
)
from app.models import MeetingRecurrence
from app.schemas.meeting_recurrence_schemas import (
    MeetingRecurrenceCreate,
    MeetingRecurrenceUpdate,
)


async def create_test_meeting_recurrence(db_session):
    meeting_recurrence = MeetingRecurrence(
        title="Test Meeting Recurrence", rrule="FREQ=DAILY;INTERVAL=1"
    )
    db_session.add(meeting_recurrence)
    await db_session.commit()
    return meeting_recurrence


@pytest.mark.asyncio
async def test_create_meeting_recurrence(test_client):
    client, db_session = test_client

    new_meeting_recurrence = MeetingRecurrenceCreate(
        title="Test Meeting Recurrence", rrule="FREQ=DAILY;INTERVAL=1"
    )
    meeting_recurrence = await create_meeting_recurrence(
        db_session, new_meeting_recurrence
    )
    assert meeting_recurrence.rrule == "FREQ=DAILY;INTERVAL=1"

    # Refresh to get updated data
    await db_session.refresh(meeting_recurrence)
    assert meeting_recurrence.rrule == "FREQ=DAILY;INTERVAL=1"


@pytest.mark.asyncio
async def test_update_meeting_recurrence(test_client):
    client, db_session = test_client

    meeting_recurrence = await create_test_meeting_recurrence(db_session)
    assert await get_meeting_recurrence(db_session, meeting_recurrence.id) is not None

    # Data to update
    update_data = MeetingRecurrenceUpdate(
        title="Updated Meeting Recurrence",
        rrule="MONTHLY;BYMONTHDAY=15;BYHOUR=9;BYMINUTE=0",
    )
    updated_meeting_recurrence = await update_meeting_recurrence(
        db_session, meeting_recurrence.id, update_data
    )
    assert updated_meeting_recurrence.title == "Updated Meeting Recurrence"

    # Refresh to get updated data
    await db_session.refresh(updated_meeting_recurrence)
    assert updated_meeting_recurrence.title == "Updated Meeting Recurrence"


@pytest.mark.asyncio
async def test_delete_meeting_recurrence(test_client):
    client, db_session = test_client

    meeting_recurrence = await create_test_meeting_recurrence(db_session)
    assert await get_meeting_recurrence(db_session, meeting_recurrence.id) is not None

    await delete_meeting_recurrence(db_session, meeting_recurrence.id)
    assert await get_meeting_recurrence(db_session, meeting_recurrence.id) is None
