from datetime import datetime

from app.crud import meeting_recurrence_crud
from dateutil.rrule import rrulestr
from sqlalchemy.ext.asyncio import AsyncSession


async def get_next_meeting_date(
    db: AsyncSession, recurrence_id: int, after_date: datetime = datetime.now()
) -> datetime:
    recurrence = await meeting_recurrence_crud.get_meeting_recurrence(db, recurrence_id)
    if not recurrence:
        return None

    # Parse the rrule string into an rrule object
    rule = rrulestr(recurrence.rrule, dtstart=after_date)

    # Fetch the next occurrence
    try:
        next_meeting_date = list(rule[:1])[0]
        return next_meeting_date
    except StopIteration:
        # Handle the case where no next date is available
        return None
