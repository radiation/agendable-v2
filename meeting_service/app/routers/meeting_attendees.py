from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, database, schemas

router = APIRouter()


@router.get("/meeting_attendees/", response_model=List[schemas.MeetingAttendee])
def read_attendees_by_meeting(meeting_id: int, db: Session = Depends(database.get_db)):
    return crud.get_attendees_by_meeting(db, meeting_id=meeting_id)


@router.get("/user_meetings/", response_model=List[schemas.Meeting])
def read_meetings_by_user(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_user_meetings(db, user_id=user_id)
