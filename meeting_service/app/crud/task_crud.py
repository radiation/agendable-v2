import datetime

import models
import schemas.task_schemas as task_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_task(db: AsyncSession, task: task_schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.Task]:
    result = await db.execute(select(models.Task).offset(skip).limit(limit))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int) -> models.Task:
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    return result.scalars().first()


async def update_task(
    db: AsyncSession, task_id: int, task: task_schemas.TaskUpdate
) -> models.Task:
    db_task = await get_task(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    db_task = await get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        await db.commit()
        return True
    return False


async def get_tasks_by_user(db: AsyncSession, user_id: int) -> list[models.Task]:
    result = await db.execute(
        select(models.Task).filter(models.Task.user_id == user_id)
    )
    return result.scalars().all()


async def mark_task_complete(db: AsyncSession, task_id: int) -> models.Task:
    task = await get_task(db, task_id)
    if not task:
        return None  # Task not found
    if task.completed:
        return False  # Task already completed
    task.completed = True
    task.completed_date = datetime.datetime.utcnow()
    db.add(task)
    await db.commit()
    return task
