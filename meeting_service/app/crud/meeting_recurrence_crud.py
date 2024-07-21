from app.models import MeetingRecurrence
from app.schemas import meeting_recurrence_schemas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_meeting_recurrence(
    db: AsyncSession,
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceBase,
) -> MeetingRecurrence:
    db_meeting_recurrence = MeetingRecurrence(**meeting_recurrence.dict())
    db.add(db_meeting_recurrence)
    await db.commit()
    await db.refresh(db_meeting_recurrence)
    return db_meeting_recurrence


async def get_meeting_recurrences(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingRecurrence]:
    stmt = select(MeetingRecurrence).offset(skip).limit(limit)
    result = await db.execute(stmt)
    recurrences = result.scalars().all()
    return recurrences


async def get_meeting_recurrence(
    db: AsyncSession, meeting_id: int
) -> MeetingRecurrence:
    result = await db.execute(
        select(MeetingRecurrence).filter(MeetingRecurrence.id == meeting_id)
    )
    recurrence = result.scalars().first()
    return recurrence


async def update_meeting_recurrence(
    db: AsyncSession,
    meeting_recurrence_id: int,
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceBase,
) -> MeetingRecurrence:
    db_meeting_recurrence = await (
        db.query(MeetingRecurrence)
        .filter(MeetingRecurrence.id == meeting_recurrence_id)
        .first()
    )
    if db_meeting_recurrence:
        for key, value in meeting_recurrence.dict().items():
            setattr(db_meeting_recurrence, key, value)
        await db.commit()
        await db.refresh(db_meeting_recurrence)
    return db_meeting_recurrence


async def delete_meeting_recurrence(
    db: AsyncSession, meeting_recurrence_id: int
) -> MeetingRecurrence:
    db_meeting_recurrence = await get_meeting_recurrence(db, meeting_recurrence_id)
    if db_meeting_recurrence:
        try:
            db.delete(db_meeting_recurrence)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_meeting_recurrence
    else:
        return None
