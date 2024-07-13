from typing import List

import crud
import db
from fastapi import APIRouter, Depends, Path
from schemas import meeting_task_schemas as schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new meeting task
@router.post("/", response_model=schemas.MeetingTask)
async def create_meeting_task(
    task: schemas.MeetingTaskCreate, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTask:
    return await crud.create_meeting_task(db=db, task=task)


# List all meeting tasks
@router.get("/", response_model=List[schemas.MeetingTask])
async def read_meeting_tasks(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> List[schemas.MeetingTask]:
    return await crud.get_meeting_tasks(db=db, skip=skip, limit=limit)


# Get a meeting task by ID
@router.get("/", response_model=schemas.MeetingTask)
async def get_meeting_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTask:
    return await crud.get_meeting_task(db=db, task_id=task_id)


# Update an existing meeting task
@router.put("/{task_id}", response_model=schemas.MeetingTask)
async def update_meeting_task(
    task_id: int, task: schemas.MeetingTaskUpdate, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTask:
    return await crud.update_meeting_task(db=db, task_id=task_id, task=task)


# Delete a meeting task
@router.delete("/{task_id}", response_model=schemas.MeetingTask)
async def delete_meeting_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTask:
    return await crud.delete_meeting_task(db=db, task_id=task_id)


# Get all tasks for a specific meeting
@router.get("/by_meeting/${meeting_id}", response_model=List[schemas.MeetingTask])
async def read_tasks_by_meeting(
    meeting_id: int = Path(
        ..., description="The ID of the meeting whose tasks are to be retrieved"
    ),
    db: AsyncSession = Depends(db.get_db),
) -> List[schemas.MeetingTask]:
    return await crud.get_tasks_by_meeting(db, meeting_id=meeting_id)
