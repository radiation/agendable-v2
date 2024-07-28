from app.models import MeetingTask, Task
from app.schemas.meeting_task_schemas import MeetingTaskCreate, MeetingTaskUpdate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_meeting_task(db: AsyncSession, task: MeetingTaskCreate) -> MeetingTask:
    db_task = MeetingTask(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_meeting_tasks(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingTask]:
    stmt = select(MeetingTask).offset(skip).limit(limit)
    result = await db.execute(stmt)
    meeting_tasks = result.scalars().all()
    return meeting_tasks


async def get_meeting_task(db: AsyncSession, meeting_task_id: int) -> MeetingTask:
    stmt = select(MeetingTask).filter(MeetingTask.id == meeting_task_id)
    result = await db.execute(stmt)
    task = result.scalars().first()
    return task


async def update_meeting_task(
    db: AsyncSession,
    meeting_task_id: int,
    meeting_task: MeetingTaskUpdate,
) -> MeetingTask:
    db_meeting_task = await get_meeting_task(db, meeting_task_id)
    if db_meeting_task:
        for key, value in meeting_task.model_dump(exclude_unset=True).items():
            setattr(db_meeting_task, key, value)
        await db.commit()
        await db.refresh(db_meeting_task)
    return db_meeting_task


async def delete_meeting_task(db: AsyncSession, meeting_task_id: int) -> MeetingTask:
    db_meeting_task = await get_meeting_task(db, meeting_task_id)
    if db_meeting_task:
        try:
            await db.delete(db_meeting_task)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_meeting_task
    else:
        return None


async def get_tasks_by_meeting(db: AsyncSession, meeting_id: int) -> list[Task]:
    stmt = (
        select(Task)
        .join(MeetingTask, MeetingTask.task_id == Task.id)
        .where(MeetingTask.meeting_id == meeting_id)
    )
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return tasks
