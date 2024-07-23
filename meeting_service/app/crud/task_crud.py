from datetime import datetime

from app.models import Task
from app.schemas import task_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_task(db: AsyncSession, task: task_schemas.TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Task]:
    stmt = select(Task).offset(skip).limit(limit)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_task(db: AsyncSession, task_id: int) -> Task:
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    return task


async def update_task(
    db: AsyncSession, task_id: int, task: task_schemas.TaskUpdate
) -> Task:
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


async def get_tasks_by_user(db: AsyncSession, user_id: int) -> list[Task]:
    result = await db.execute(select(Task).filter(Task.user_id == user_id))
    return result.scalars().all()


async def mark_task_complete(db: AsyncSession, task_id: int) -> Task:
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
