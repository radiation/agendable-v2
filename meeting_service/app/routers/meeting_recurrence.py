from typing import List

import crud
import db
from fastapi import APIRouter, Depends
from schemas import meeting_task_schemas as schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("meeting_recurrence/", response_model=schemas.MeetingTask)
def get_meeting_recurrence(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> schemas.MeetingTask:
    return crud.get_meeting_recurrence(db=db, meeting_id=meeting_id)


@router.get("/meeting_tasks/", response_model=List[schemas.MeetingTask])
def read_tasks_by_meeting(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> List[schemas.MeetingTask]:
    return crud.get_tasks_by_meeting(db, meeting_id=meeting_id)
