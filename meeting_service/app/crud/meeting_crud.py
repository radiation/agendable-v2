import models
import schemas.meeting_schemas as schemas
from sqlalchemy.orm import Session


def get_meeting(db: Session, meeting_id: int):
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()


def get_meetings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meeting).offset(skip).limit(limit).all()


def create_meeting(db: Session, meeting: schemas.MeetingCreate) -> models.Meeting:
    db_meeting = models.Meeting(**meeting.model_dump)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def update_meeting(
    db: Session, meeting_id: int, meeting: schemas.MeetingUpdate
) -> models.Meeting:
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        for key, value in meeting.model_dump(exclude_unset=True).items():
            setattr(db_meeting, key, value)
        db.commit()
        db.refresh(db_meeting)
    return db_meeting


def delete_meeting(db: Session, meeting_id: int) -> models.Meeting:
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        db.delete(db_meeting)
        db.commit()
    return db_meeting


def get_meeting_recurrence_by_meeting(
    db: Session, meeting_id: int
) -> models.MeetingRecurrence:
    return (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.meetings.any(id=meeting_id))
        .first()
    )


def get_next_occurrence(db: Session, meeting_id: int) -> models.Meeting:
    meeting = get_meeting(db, meeting_id)
    if meeting:
        pass


def complete_meeting(db: Session, meeting_id: int):
    meeting = get_meeting(db, meeting_id)
    if meeting:
        # TODO: Implement this
        return meeting


def add_recurrence(db: Session, meeting_id: int, recurrence_id: int):
    meeting = get_meeting(db, meeting_id)
    if meeting:
        recurrence = (
            db.query(models.MeetingRecurrence)
            .filter(models.MeetingRecurrence.id == recurrence_id)
            .first()
        )
        if recurrence:
            meeting.recurrence = recurrence
            db.commit()
            db.refresh(meeting)
            return meeting
    return None
