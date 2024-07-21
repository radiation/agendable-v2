from app.models import Meeting, MeetingRecurrence
from app.schemas import meeting_schemas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


async def create_meeting(
    db: AsyncSession, meeting: meeting_schemas.MeetingCreate
) -> Meeting:
    db_meeting = Meeting(**meeting.dict())
    db.add(db_meeting)
    await db.commit()
    await db.refresh(db_meeting)
    if db_meeting.recurrence_id:
        db_meeting = await db.get(
            Meeting, db_meeting.id, options=[joinedload(Meeting.recurrence)]
        )
    return db_meeting


async def get_meetings(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[Meeting]:
    stmt = (
        select(Meeting)
        .options(joinedload(Meeting.recurrence))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    meetings = result.scalars().all()
    return meetings


async def get_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    stmt = (
        select(Meeting)
        .options(joinedload(Meeting.recurrence))
        .filter(Meeting.id == meeting_id)
    )
    result = await db.execute(stmt)
    meeting = result.scalars().first()
    return meeting


async def update_meeting(
    db: AsyncSession, meeting_id: int, meeting: meeting_schemas.MeetingUpdate
) -> Meeting:
    db_meeting = await get_meeting(db, meeting_id)
    if db_meeting:
        for key, value in meeting.dict(exclude_unset=True).items():
            setattr(db_meeting, key, value)
        await db.commit()
        await db.refresh(db_meeting)
    return db_meeting


async def delete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    db_meeting = await get_meeting(db, meeting_id)
    if db_meeting:
        try:
            db.delete(db_meeting)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_meeting
    else:
        return None


async def get_meeting_recurrence_by_meeting(
    db: AsyncSession, meeting_id: int
) -> MeetingRecurrence:
    result = await db.execute(
        select(MeetingRecurrence).filter(MeetingRecurrence.meeting_id == meeting_id)
    )
    recurrence = result.scalars().first()
    return recurrence


async def complete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    meeting = await get_meeting(db, meeting_id)
    if meeting:
        meeting.completed = True
        await db.commit()
        await db.refresh(meeting)
        return meeting


async def add_recurrence(
    db: AsyncSession, meeting_id: int, recurrence_id: int
) -> Meeting:
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    if meeting.recurrence_id is not None:
        # We don't want to add a recurrence to a meeting that already has one
        return meeting

    recurrence_exists = await db.scalar(
        select(MeetingRecurrence.id).filter(MeetingRecurrence.id == recurrence_id)
    )

    if not recurrence_exists:
        raise ValueError("Recurrence not found")

    meeting.recurrence_id = recurrence_id
    await db.commit()
    await db.refresh(meeting)
    return meeting
