from models import Meeting, MeetingRecurrence
from schemas import meeting_schemas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    result = await db.execute(select(Meeting).filter(Meeting.id == meeting_id))
    meeting = result.scalars().first()
    return meeting


async def get_meetings(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[Meeting]:
    return await db.query(Meeting).offset(skip).limit(limit).all()


async def create_meeting(
    db: AsyncSession, meeting: meeting_schemas.MeetingCreate
) -> Meeting:
    db_meeting = Meeting(**meeting.model_dump)
    db.add(db_meeting)
    await db.commit()
    await db.refresh(db_meeting)
    return db_meeting


async def update_meeting(
    db: AsyncSession, meeting_id: int, meeting: meeting_schemas.MeetingUpdate
) -> Meeting:
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        for key, value in meeting.model_dump(exclude_unset=True).items():
            setattr(db_meeting, key, value)
        await db.commit()
        await db.refresh(db_meeting)
    return db_meeting


async def delete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    # First, await the retrieval of the meeting
    db_meeting = await get_meeting(db, meeting_id)
    if db_meeting:
        try:
            db.delete(db_meeting)
            await db.commit()
        except SQLAlchemyError as e:
            # Optionally handle specific database errors, e.g., rollback, logging, etc.
            await db.rollback()
            raise e
        return db_meeting
    else:
        # Raise an exception or return None if the meeting doesn't exist
        return None


def get_meeting_recurrence_by_meeting(
    db: AsyncSession, meeting_id: int
) -> MeetingRecurrence:
    return (
        db.query(MeetingRecurrence)
        .filter(MeetingRecurrence.meetings.any(id=meeting_id))
        .first()
    )


def get_next_occurrence(db: AsyncSession, meeting_id: int) -> Meeting:
    meeting = get_meeting(db, meeting_id)
    if meeting:
        pass


def complete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    meeting = get_meeting(db, meeting_id)
    if meeting:
        # TODO: Implement this
        return meeting


def add_recurrence(db: AsyncSession, meeting_id: int, recurrence_id: int) -> Meeting:
    meeting = get_meeting(db, meeting_id)
    if meeting:
        recurrence = (
            db.query(MeetingRecurrence)
            .filter(MeetingRecurrence.id == recurrence_id)
            .first()
        )
        if recurrence:
            meeting.recurrence = recurrence
            db.commit()
            db.refresh(meeting)
            return meeting
    return None
