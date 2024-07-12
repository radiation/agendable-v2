import models
import schemas.meeting_attendee_schemas as meeting_attendee_schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def create_meeting_attendee(
    db: AsyncSession, attendee: meeting_attendee_schemas.MeetingAttendeeCreate
) -> models.MeetingAttendee:
    db_attendee = models.MeetingAttendee(**attendee.dict())
    db.add(db_attendee)
    await db.commit()
    await db.refresh(db_attendee)
    return db_attendee


async def get_meeting_attendees(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.MeetingAttendee]:
    return await db.query(models.MeetingAttendee).offset(skip).limit(limit).all()


async def get_meeting_attendee(
    db: AsyncSession, attendee_id: int
) -> models.MeetingAttendee:
    return await (
        db.query(models.MeetingAttendee)
        .filter(models.MeetingAttendee.id == attendee_id)
        .first()
    )


async def update_meeting_attendee(
    db: AsyncSession,
    attendee_id: int,
    attendee: meeting_attendee_schemas.MeetingAttendeeUpdate,
) -> models.MeetingAttendee:
    db_attendee = await get_meeting_attendee(db, attendee_id)
    if db_attendee:
        for key, value in attendee.dict(exclude_unset=True).items():
            setattr(db_attendee, key, value)
        await db.commit()
        await db.refresh(db_attendee)
    return db_attendee


async def delete_meeting_attendee(
    db: AsyncSession, attendee_id: int
) -> models.MeetingAttendee:
    db_attendee = await get_meeting_attendee(db, attendee_id)
    if db_attendee:
        db.delete(db_attendee)
        await db.commit()
        return db_attendee
    else:
        return None


async def get_attendees_by_meeting(
    db: AsyncSession, meeting_id: int
) -> list[models.MeetingAttendee]:
    return await (
        db.query(models.MeetingAttendee)
        .filter(models.MeetingAttendee.meeting_id == meeting_id)
        .all()
    )
