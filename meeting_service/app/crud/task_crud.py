import models
import schemas.task_schemas as task_schemas
from sqlalchemy.orm import Session


def get_task(db: Session, task_id: int) -> models.Task:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 10) -> list[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: task_schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
