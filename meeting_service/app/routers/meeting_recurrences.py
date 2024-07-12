import crud
import db
from fastapi import APIRouter, Depends
from schemas import meeting_task_schemas as schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=schemas.MeetingTask)
def get_meeting_recurrence(
    meeting_id: int, db: Session = Depends(db.get_db)
) -> schemas.MeetingTask:
    return crud.get_meeting_recurrence(db=db, meeting_id=meeting_id)
