from models import MeetingTask
from schemas import meeting_task_schemas
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_meeting_task(
    db: AsyncSession, task: meeting_task_schemas.MeetingTaskCreate
) -> MeetingTask:
    db_task = MeetingTask(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_meeting_tasks(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingTask]:
    stmt = select(MeetingTask).offset(skip).limit(limit)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_meeting_task(db: AsyncSession, task_id: int) -> MeetingTask:
    result = await db.execute(select(MeetingTask).filter(MeetingTask.id == task_id))
    task = result.scalars().first()
    return task


async def update_meeting_task(
    db: AsyncSession, task_id: int, task: meeting_task_schemas.MeetingTaskUpdate
) -> MeetingTask:
    db_task = get_meeting_task(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_meeting_task(db: AsyncSession, task_id: int) -> MeetingTask:
    db_task = get_meeting_task(db, task_id)
    if db_task:
        try:
            db.delete(db_task)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_task
    else:
        return None


async def get_tasks_by_meeting(db: AsyncSession, meeting_id: int) -> list[MeetingTask]:
    result = await db.execute(
        select(MeetingTask).where(MeetingTask.meeting_id == meeting_id)
    )
    return result.scalars().all()
