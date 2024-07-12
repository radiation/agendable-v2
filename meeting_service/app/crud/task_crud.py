import models
import schemas.task_schemas as task_schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def get_task(db: AsyncSession, task_id: int) -> models.Task:
    return await db.query(models.Task).filter(models.Task.id == task_id).first()


async def get_tasks(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.Task]:
    return await db.query(models.Task).offset(skip).limit(limit).all()


async def create_task(db: AsyncSession, task: task_schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task
