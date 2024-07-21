from datetime import datetime

from app.crud import meeting_crud, meeting_task_crud
from app.models import Meeting, MeetingTask
from app.schemas import meeting_schemas
from app.services import meeting_recurrence_service
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


# Get the next meeting in the series whose start date is after the given date
async def get_subsequent_meeting(
    db: AsyncSession, meeting: Meeting, after_date: datetime = datetime.now()
) -> Meeting:
    if not meeting.recurrence_id:
        raise ValueError(f"Meeting {meeting} does not have a recurrence set")

    # Check if there's a meeting after the given date
    result = await db.execute(
        select(Meeting)
        .filter(
            and_(
                Meeting.recurrence_id == meeting.recurrence_id,
                Meeting.start_date > after_date,
            )
        )
        .order_by(Meeting.start_date.asc())
    )
    next_meeting = result.scalars().first()

    # If there's no meeting after the given date, create the next meeting
    if not next_meeting:
        return await create_subsequent_meeting(db, meeting)
    else:
        return next_meeting


async def create_subsequent_meeting(db: AsyncSession, meeting: Meeting) -> Meeting:
    if not meeting or not meeting.recurrence:
        return None  # Handle error if meeting not found or recurrence not set

    next_meeting_date = await meeting_recurrence_service.get_next_meeting_date(
        db, meeting.recurrence_id, meeting.start_date
    )
    if not next_meeting_date:
        return None  # TODO: Handle error if next meeting date not found

    # Calculate the end date based on the duration if applicable
    if meeting.end_date and meeting.start_date:
        duration = meeting.end_date - meeting.start_date
        next_meeting_end_date = next_meeting_date + duration
    else:
        next_meeting_end_date = None

    # Create a MeetingCreate schema object
    meeting_data = meeting_schemas.MeetingCreate(
        title=meeting.title,
        start_date=next_meeting_date,
        end_date=next_meeting_end_date,
        duration=meeting.duration,
        location=meeting.location,
        notes=meeting.notes,
        num_reschedules=0,
        reminder_sent=False,
    )

    # Use the meeting_crud to create the new meeting
    new_meeting = await meeting_crud.create_meeting(db, meeting_data)
    return new_meeting


async def complete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    meeting = await meeting_crud.get_meeting(db, meeting_id)
    if not meeting:
        return None  # TODO: handle error if meeting not found

    # Mark the meeting as completed
    meeting.completed = True

    # Retrieve tasks for the current meeting
    meeting_tasks: list[MeetingTask] = meeting_task_crud.get_tasks_by_meeting(
        db, meeting_id
    )

    # Assuming there's a function to find the next meeting in the series
    next_meeting_id = await get_subsequent_meeting(db, meeting.recurrence_id)

    # Update tasks if next meeting is available
    if next_meeting_id:
        for meeting_task in meeting_tasks:
            if not meeting_task.completed:
                meeting_task.meeting_id = next_meeting_id
                # Add logic to update task status if necessary

    # Commit all changes at once
    await db.commit()
    await db.refresh(meeting)
    return meeting
