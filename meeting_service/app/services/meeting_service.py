from datetime import datetime

from crud import meeting_crud, meeting_task_crud
from models import Meeting, MeetingTask
from services import meeting_recurrence_service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_next_meeting(
    db: AsyncSession, recurrence_id: int, after_date: datetime = None
) -> Meeting:
    next_meeting_date = await meeting_recurrence_service.get_next_meeting_date(
        db, recurrence_id, after_date
    )
    if not next_meeting_date:
        return None  # TODO: Handle error if next meeting date not found

    # Get the next meeting in the series
    result = await db.execute(
        select(Meeting).filter(
            Meeting.recurrence_id == recurrence_id,
            Meeting.start_date == next_meeting_date,
        )
    )
    next_meeting = result.scalars().first()
    return next_meeting


async def create_next_meeting_from_recurrence(
    db: AsyncSession, meeting_id: int
) -> Meeting:
    meeting = await meeting_crud.get_meeting(db, meeting_id)
    if not meeting or not meeting.recurrence:
        return None  # TODO: Handle error if meeting not found or recurrence not set

    next_meeting_date = await meeting_recurrence_service.get_next_meeting_date(
        db, meeting.recurrence_id, meeting.start_date
    )
    if not next_meeting_date:
        return None  # TODO: Handle error if next meeting date not found

    # Get next meeting in the series
    new_meeting = await get_next_meeting(db, meeting_id, next_meeting_date)
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
    next_meeting_id = await get_next_meeting(db, meeting.recurrence_id)

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
