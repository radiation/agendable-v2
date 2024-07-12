import models
import schemas.meeting_attendee_schemas as meeting_attendee_schemas
from sqlalchemy.orm import Session


def get_meeting_attendee(db: Session, attendee_id: int) -> models.MeetingAttendee:
    return (
        db.query(models.MeetingAttendee)
        .filter(models.MeetingAttendee.id == attendee_id)
        .first()
    )


def get_meeting_attendees(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.MeetingAttendee]:
    return db.query(models.MeetingAttendee).offset(skip).limit(limit).all()


def create_meeting_attendee(
    db: Session, attendee: meeting_attendee_schemas.MeetingAttendeeCreate
) -> models.MeetingAttendee:
    db_attendee = models.MeetingAttendee(**attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee


def get_attendees_by_meeting(
    db: Session, meeting_id: int
) -> list[models.MeetingAttendee]:
    return (
        db.query(models.MeetingAttendee)
        .filter(models.MeetingAttendee.meeting_id == meeting_id)
        .all()
    )
