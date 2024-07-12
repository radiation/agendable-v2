import models
import schemas.meeting_task_schemas as meeting_task_schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def create_meeting_task(
    db: AsyncSession, task: meeting_task_schemas.MeetingTaskCreate
) -> models.MeetingTask:
    db_task = models.MeetingTask(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_meeting_tasks(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.MeetingTask]:
    return await db.query(models.MeetingTask).offset(skip).limit(limit).all()


async def get_meeting_task(db: AsyncSession, task_id: int) -> models.MeetingTask:
    return (
        await db.query(models.MeetingTask)
        .filter(models.MeetingTask.id == task_id)
        .first()
    )


async def update_meeting_task(
    db: AsyncSession, task_id: int, task: meeting_task_schemas.MeetingTaskUpdate
) -> models.MeetingTask:
    db_task = get_meeting_task(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_meeting_task(db: AsyncSession, task_id: int) -> models.MeetingTask:
    db_task = get_meeting_task(db, task_id)
    if db_task:
        db.delete(db_task)
        await db.commit()
        return db_task
    else:
        return None


async def get_tasks_by_meeting(
    db: AsyncSession, meeting_id: int
) -> list[models.MeetingTask]:
    return await (
        db.query(models.MeetingTask)
        .filter(models.MeetingTask.meeting_id == meeting_id)
        .all()
    )
