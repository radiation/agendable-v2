from typing import List

import crud
import db
from fastapi import APIRouter, Depends, Path
from schemas import meeting_task_schemas as schemas
from sqlalchemy.orm import Session

router = APIRouter()


# List all meeting tasks
@router.get("/", response_model=List[schemas.MeetingTask])
def read_meeting_tasks(
    skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)
) -> List[schemas.MeetingTask]:
    return crud.get_meeting_tasks(db=db, skip=skip, limit=limit)


# Get a meeting task by ID
@router.get("/", response_model=schemas.MeetingTask)
def get_meeting_task(
    task_id: int, db: Session = Depends(db.get_db)
) -> schemas.MeetingTask:
    return crud.get_meeting_task(db=db, task_id=task_id)


# Create a new meeting task
@router.post("/", response_model=schemas.MeetingTask)
def create_meeting_task(
    task: schemas.MeetingTaskCreate, db: Session = Depends(db.get_db)
) -> schemas.MeetingTask:
    return crud.create_meeting_task(db=db, task=task)


# Update an existing meeting task
@router.put("/{task_id}", response_model=schemas.MeetingTask)
def update_meeting_task(
    task_id: int, task: schemas.MeetingTaskUpdate, db: Session = Depends(db.get_db)
) -> schemas.MeetingTask:
    return crud.update_meeting_task(db=db, task_id=task_id, task=task)


# Delete a meeting task
@router.delete("/{task_id}", response_model=schemas.MeetingTask)
def delete_meeting_task(
    task_id: int, db: Session = Depends(db.get_db)
) -> schemas.MeetingTask:
    return crud.delete_meeting_task(db=db, task_id=task_id)


# Get all tasks for a specific meeting
@router.get("/by_meeting/${meeting_id}", response_model=List[schemas.MeetingTask])
def read_tasks_by_meeting(
    meeting_id: int = Path(
        ..., description="The ID of the meeting whose tasks are to be retrieved"
    ),
    db: Session = Depends(db.get_db),
) -> List[schemas.MeetingTask]:
    return crud.get_tasks_by_meeting(db, meeting_id=meeting_id)
