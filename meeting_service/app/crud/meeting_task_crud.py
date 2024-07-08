import models
import schemas
from sqlalchemy.orm import Session


def get_meeting_task(db: Session, task_id: int):
    return db.query(models.MeetingTask).filter(models.MeetingTask.id == task_id).first()


def get_meeting_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MeetingTask).offset(skip).limit(limit).all()


def create_meeting_task(db: Session, task: schemas.MeetingTaskCreate):
    db_task = models.MeetingTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_meeting(db: Session, meeting_id: int):
    return (
        db.query(models.MeetingTask)
        .filter(models.MeetingTask.meeting_id == meeting_id)
        .all()
    )
