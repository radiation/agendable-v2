import models
import schemas
from sqlalchemy.orm import Session

"""
Meeting CRUD
"""


def get_meeting(db: Session, meeting_id: int):
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()


def get_meetings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meeting).offset(skip).limit(limit).all()


def create_meeting(db: Session, meeting: schemas.MeetingCreate):
    db_meeting = models.Meeting(**meeting.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def update_meeting(db: Session, meeting_id: int, meeting: schemas.MeetingUpdate):
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        for key, value in meeting.dict(exclude_unset=True).items():
            setattr(db_meeting, key, value)
        db.commit()
        db.refresh(db_meeting)
    return db_meeting


def delete_meeting(db: Session, meeting_id: int):
    db_meeting = get_meeting(db, meeting_id)
    if db_meeting:
        db.delete(db_meeting)
        db.commit()
    return db_meeting


def get_meeting_recurrence_by_meeting(db: Session, meeting_id: int):
    return (
        db.query(models.MeetingRecurrence)
        .filter(models.MeetingRecurrence.meetings.any(id=meeting_id))
        .first()
    )


def get_next_occurrence(db: Session, meeting_id: int):
    meeting = get_meeting(db, meeting_id)
    if meeting:
        # Implement your logic to get the next occurrence
        pass


def complete_meeting(db: Session, meeting_id: int):
    meeting = get_meeting(db, meeting_id)
    if meeting:
        # Implement your logic to complete the meeting
        pass


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


"""
Meeting Recurrence CRUD
"""


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
