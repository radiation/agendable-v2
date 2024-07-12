import models
import schemas.meeting_recurrence_schemas as meeting_recurrence_schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def create_meeting_recurrence(
    db: AsyncSession,
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceBase,
) -> models.MeetingRecurrence:
    db_meeting_recurrence = models.MeetingRecurrence(**meeting_recurrence.model_dump)
    db.add(db_meeting_recurrence)
    await db.commit()
    await db.refresh(db_meeting_recurrence)
    return db_meeting_recurrence


async def get_meeting_recurrences(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.MeetingRecurrence]:
    return await db.query(models.MeetingRecurrence).offset(skip).limit(limit).all()


async def get_meeting_recurrence(
    db: AsyncSession, meeting_id: int
) -> models.MeetingRecurrence:
    return await (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.meetings.any(id=meeting_id))
        .first()
    )


async def update_meeting_recurrence(
    db: AsyncSession,
    meeting_recurrence_id: int,
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceBase,
) -> models.MeetingRecurrence:
    db_meeting_recurrence = await (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.id == meeting_recurrence_id)
        .first()
    )
    if db_meeting_recurrence:
        for key, value in meeting_recurrence.model_dump(exclude_unset=True).items():
            setattr(db_meeting_recurrence, key, value)
        await db.commit()
        await db.refresh(db_meeting_recurrence)
    return db_meeting_recurrence


async def delete_meeting_recurrence(
    db: AsyncSession, meeting_recurrence_id: int
) -> models.MeetingRecurrence:
    db_meeting_recurrence = await (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.id == meeting_recurrence_id)
        .first()
    )
    if db_meeting_recurrence:
        db.delete(db_meeting_recurrence)
        await db.commit()
        return db_meeting_recurrence
    else:
        return None
