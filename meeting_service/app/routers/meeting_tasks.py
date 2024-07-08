from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, database, schemas

router = APIRouter()


@router.get("/meeting_tasks/", response_model=List[schemas.MeetingTask])
def read_tasks_by_meeting(meeting_id: int, db: Session = Depends(database.get_db)):
    return crud.get_tasks_by_meeting(db, meeting_id=meeting_id)
