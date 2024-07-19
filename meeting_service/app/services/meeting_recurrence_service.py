from datetime import datetime

from crud import meeting_recurrence_crud
from dateutil.rrule import MONTHLY, rrule
from sqlalchemy.ext.asyncio import AsyncSession


async def get_next_meeting_date(
    db: AsyncSession, recurrence_id: int, after_date: datetime = None
) -> datetime:
    recurrence = await meeting_recurrence_crud.get_meeting_recurrence(db, recurrence_id)
    if not recurrence:
        return None

    # Convert recurrence pattern into dateutil.rrule
    rule = rrule(
        freq=MONTHLY,
        dtstart=after_date or datetime.now(),
        interval=recurrence.interval,
        count=1,
    )
    next_meeting_date = next(rule)
    return next_meeting_date
