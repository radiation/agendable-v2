from datetime import datetime

from app.crud import meeting_crud
from app.models import MeetingTask, Task
from app.services import meeting_service
from sqlalchemy.ext.asyncio import AsyncSession


# Create a new task and assign it to a meeting via a meeting task
async def create_new_meeting_task(
    db: AsyncSession,
    meeting_id: int,
    task_title: str,
    assignee_id: int,
    due_date: datetime = None,
) -> MeetingTask:
    # Fetch the meeting and check for the next meeting in its recurrence
    meeting = await meeting_crud.get_meeting(db, meeting_id)
    if not meeting:
        raise ValueError(f"Meeting with ID {meeting_id} not found")

    # Get the due date for the task
    if not due_date:
        next_meeting = await meeting_service.get_subsequent_meeting(
            db, meeting.recurrence_id, after_date=meeting.end_date
        )
        due_date = next_meeting.start_date if next_meeting else None

    # Create the task with the due date set to the next meeting date
    new_task = Task(title=task_title, assignee_id=assignee_id, due_date=due_date)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    # Link the task with the meeting
    new_meeting_task = MeetingTask(meeting_id=meeting_id, task_id=new_task.id)
    db.add(new_meeting_task)
    await db.commit()
    await db.refresh(new_meeting_task)

    return new_meeting_task
