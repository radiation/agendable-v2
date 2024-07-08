import models
import schemas
from sqlalchemy.orm import Session


def get_meeting_recurrence(db: Session, meeting_id: int):
    return (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.meetings.any(id=meeting_id))
        .first()
    )


def get_meeting_recurrences(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MeetingRecurrence).offset(skip).limit(limit).all()


def create_meeting_recurrence(
    db: Session, meeting_recurrence: schemas.MeetingRecurrenceBase
):
    db_meeting_recurrence = models.MeetingRecurrence(**meeting_recurrence.dict())
    db.add(db_meeting_recurrence)
    db.commit()
    db.refresh(db_meeting_recurrence)
    return db_meeting_recurrence


def update_meeting_recurrence(
    db: Session,
    meeting_recurrence_id: int,
    meeting_recurrence: schemas.MeetingRecurrenceBase,
):
    db_meeting_recurrence = (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.id == meeting_recurrence_id)
        .first()
    )
    if db_meeting_recurrence:
        for key, value in meeting_recurrence.dict(exclude_unset=True).items():
            setattr(db_meeting_recurrence, key, value)
        db.commit()
        db.refresh(db_meeting_recurrence)
    return db_meeting_recurrence


def create_meeting_task(db: Session, meeting_task: schemas.MeetingTaskCreate):
    db_meeting_task = models.MeetingTask(**meeting_task.dict())
    db.add(db_meeting_task)
    db.commit()
    db.refresh(db_meeting_task)
    return db_meeting_task
