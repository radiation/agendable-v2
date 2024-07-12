import models
import schemas.meeting_task_schemas as meeting_task_schemas
from sqlalchemy.orm import Session


def get_meeting_task(db: Session, task_id: int) -> models.MeetingTask:
    return db.query(models.MeetingTask).filter(models.MeetingTask.id == task_id).first()


def get_meeting_tasks(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.MeetingTask]:
    return db.query(models.MeetingTask).offset(skip).limit(limit).all()


def create_meeting_task(
    db: Session, task: meeting_task_schemas.MeetingTaskCreate
) -> models.MeetingTask:
    db_task = models.MeetingTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_meeting(db: Session, meeting_id: int) -> list[models.MeetingTask]:
    return (
        db.query(models.MeetingTask)
        .filter(models.MeetingTask.meeting_id == meeting_id)
        .all()
    )
