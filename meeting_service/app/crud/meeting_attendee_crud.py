from models import MeetingAttendee
from schemas import meeting_attendee_schemas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_meeting_attendee(
    db: AsyncSession, attendee: meeting_attendee_schemas.MeetingAttendeeCreate
) -> MeetingAttendee:
    db_attendee = MeetingAttendee(**attendee.dict())
    db.add(db_attendee)
    await db.commit()
    await db.refresh(db_attendee)
    return db_attendee


async def get_meeting_attendees(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingAttendee]:
    stmt = select(MeetingAttendee).offset(skip).limit(limit)
    result = await db.execute(stmt)
    attendees = result.scalars().all()
    return attendees


async def get_meeting_attendee(db: AsyncSession, attendee_id: int) -> MeetingAttendee:
    result = await db.execute(
        select(MeetingAttendee).filter(MeetingAttendee.id == attendee_id)
    )
    attendee = result.scalars().first()
    return attendee


async def update_meeting_attendee(
    db: AsyncSession,
    attendee_id: int,
    attendee: meeting_attendee_schemas.MeetingAttendeeUpdate,
) -> MeetingAttendee:
    db_attendee = await get_meeting_attendee(db, attendee_id)
    if db_attendee:
        for key, value in attendee.dict(exclude_unset=True).items():
            setattr(db_attendee, key, value)
        await db.commit()
        await db.refresh(db_attendee)
    return db_attendee


async def delete_meeting_attendee(
    db: AsyncSession, attendee_id: int
) -> MeetingAttendee:
    db_attendee = await get_meeting_attendee(db, attendee_id)
    if db_attendee:
        try:
            db.delete(db_attendee)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_attendee
    else:
        return None


async def get_attendees_by_meeting(
    db: AsyncSession, meeting_id: int
) -> list[MeetingAttendee]:
    return await (
        db.query(MeetingAttendee).filter(MeetingAttendee.meeting_id == meeting_id).all()
    )
